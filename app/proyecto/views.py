import os
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from django.utils import timezone

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.db.models import Prefetch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.platypus import Spacer

from solicitud.models import Postulacion

from proyecto.models import (DatosProyectoBase, Justificacion, Idea_Proyecto, Objetivo_especifico, Beneficiario,
                             Modelo_Acta, Derecho_propietario, Impacto_ambiental, Riesgo_desastre, Detalle_POA,
                             Conclusion_recomendacion, Declaracion_jurada, PresupuestoReferencial)

class Lista_Proyectos(ListView):
    model = Postulacion
    template_name = 'Proyecto/lista.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_Proyectos, self).get_context_data(**kwargs)
        proyectos = self.model.objects.filter(estado=True)
        context['titulo'] = 'LISTA DE PROYECTOS CON INICIO DE SESION'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS CON INICIO DE SESION'
        context['object_list'] = proyectos
        return context
    
def generate_pdf(request, slug):
    # Creamos una respuesta HttpResponse para devolver el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="proyecto_detalles_{slug}.pdf"'

    # Crear el objeto SimpleDocTemplate
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Obtener los objetos Postulacion y DatosProyectoBase usando el slug
    try:
        postulacion = Postulacion.objects.get(slug=slug)
        proyecto = DatosProyectoBase.objects.get(slug=slug)
        justificacion = Justificacion.objects.get(slug=slug)
        idea = Idea_Proyecto.objects.get(slug=slug)
        objetivo = Objetivo_especifico.objects.filter(slug=slug)
        beneficiarios = Beneficiario.objects.get(slug=slug)
        modelo = Modelo_Acta.objects.filter(slug=slug)
        derecho = Derecho_propietario.objects.filter(slug=slug)
        impacto = Impacto_ambiental.objects.get(slug=slug)
        riesgo = Riesgo_desastre.objects.filter(slug=slug)
        poa = Detalle_POA.objects.get(slug=slug)
        conclusion = Conclusion_recomendacion.objects.get(slug=slug)
        declaracion = Declaracion_jurada.objects.get(slug=slug)
        presupuesto = PresupuestoReferencial.objects.get(slug=slug)
    except (Postulacion.DoesNotExist, DatosProyectoBase.DoesNotExist, Justificacion.DoesNotExist, Idea_Proyecto.DoesNotExist,
            Objetivo_especifico.DoesNotExist, Beneficiario.DoesNotExist, Modelo_Acta.DoesNotExist, Derecho_propietario.DoesNotExist,
            Impacto_ambiental.DoesNotExist, Riesgo_desastre.DoesNotExist, Detalle_POA.DoesNotExist, Conclusion_recomendacion.DoesNotExist,
            Declaracion_jurada.DoesNotExist, PresupuestoReferencial.DoesNotExist):
        return HttpResponse("Los datos no fueron encontrados para este slug.", status=404)
    
    # Estilos personalizados
    style_right = ParagraphStyle(
        name='RightAlignStyle',
        fontName='Helvetica-Bold',
        fontSize=7,
        alignment=2,  # Alineación a la derecha
        textColor=colors.black,
        spaceAfter=2,
    )

    style_center = ParagraphStyle(
        name='CenterAlignStyle',
        fontName='Helvetica-Bold',
        fontSize=14,
        alignment=1,  # Alineación centrada
        textColor=colors.black,
        spaceAfter=22,
    )

    style_left = ParagraphStyle(
        name='LeftAlignStyle',
        fontName='Helvetica-Bold',
        fontSize=8,
        alignment=0,  # Alineación a la izquierda
        textColor=colors.black,
        spaceAfter=8,
    )

    # Título de la convocatoria
    convocatoria = f"{postulacion.convocatoria.nombre}"
    convocatoria_title = Paragraph(convocatoria, style_right)
    elements.append(convocatoria_title)

    # Título del documento
    title = f"<u>Informe Técnico de Condiciones Previas</u>"
    title_paragraph = Paragraph(title, style_center)
    elements.append(title_paragraph)

    # Título de sección
    subt0 = f"0.- DATOS DE CONTACTO DEL PROYECTO:"
    subt0_title = Paragraph(subt0, style_left)
    elements.append(subt0_title)

    # -------------------------
    # Tabla de contactos del proyecto
    # -------------------------
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_normal.fontName = 'Helvetica'
    style_normal.fontSize = 7  # Tamaño de la fuente para las celdas
    style_normal.alignment = 1  # Alineación horizontal centrado (1 = centrado)
    style_normal.valign = 'middle'  # Alineación vertical en el medio
    style_normal.justification = 'CENTER'  # O 'CENTER' o 'RIGHT' según sea necesario
    style_normal.leading = 8  # Controla la separación entre las líneas (reduce el espacio entre las líneas)

    # Estilo de la tabla
    table_style = [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación de todo el texto al centro
        ('FONTSIZE', (0, 0), (-1, -1), 7),  # Establecer el tamaño de la fuente globalmente
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Títulos en negrita
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Resto de las celdas con fuente normal
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),  # Padding en los títulos
        ('TOPPADDING', (0, 1), (-1, -1), 3),  # Padding en el contenido
        #('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fondo gris para los títulos
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical en el medio de las celdas
    ]

    stylesl = getSampleStyleSheet()
    style_lef = stylesl['Normal']
    style_lef.fontName = 'Helvetica'
    style_lef.fontSize = 7  # Tamaño de la fuente para las celdas
    style_lef.alignment = 0  # Alineación horizontal centrado (1 = centrado)
    style_lef.valign = 'middle'  # Alineación vertical en el medio
    style_lef.justification = 'LEFT'  # O 'CENTER' o 'RIGHT' según sea necesario
    style_lef.leading = 8  # Controla la separación entre las líneas (reduce el espacio entre las líneas)

    table_style_V = [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación de todo el texto al centro
        ('FONTSIZE', (0, 0), (-1, -1), 7),  # Establecer el tamaño de la fuente globalmente
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Títulos en negrita
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Resto de las celdas con fuente normal
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),  # Padding en los títulos
        ('TOPPADDING', (0, 1), (-1, -1), 3),  # Padding en el contenido
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical en el medio de las celdas
    ]
     # Crear los datos para la tabla
    data_municipio = [
        ["CODIGO PROYECTO", "DEPARTAMENTO", "ETA", "MUNICIPIO"]
    ]
    data_municipio.append([
        str(postulacion.slug),
        str(postulacion.municipio.departamento),
        str(postulacion.municipio.entidad_territorial),
        str(postulacion.municipio.nombre_municipio),
    ])

    # Convertir cada valor de la tabla en un Paragraph para que el texto se ajuste dentro de las celdas
    data_municipio = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_municipio]
    table_municipio = Table(data_municipio, colWidths=[130, 130, 130, 130], rowHeights=25)# Crear la tabla
    # Aplicar estilo
    table_municipio.setStyle(table_style)
    # Permitir que el texto se ajuste y se divida en varias filas si es necesario
    table_municipio.splitByRow = True  # Esto asegura que el texto largo se divida en varias filas
    elements.append(table_municipio)

    # Agregar un Spacer para separar las tablas (separación de 12 puntos de altura)
    elements.append(Spacer(1, 8))  # 1 es el ancho (puede ser 0), 12 es la altura (ajústalo según lo necesario)

    # -------------------------
    # Tabla de MAE
    # -------------------------

    data_mae = [
        ["NOMBRE MAE", "CARGO MAE", "CELULAR MAE", "CORREO DOMICILIO LEGAL PARA NOTIFICACION"]
    ]
    data_mae.append([
        str(postulacion.mae.persona.nombrecompleto()),
        str(postulacion.mae.persona.cargo),
        str(postulacion.mae.persona.celular),
        str(postulacion.mae.correo),
    ])

    data_mae = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_mae]
    table_mae = Table(data_mae, colWidths=[130, 130, 130, 130], rowHeights=25)
    table_mae.setStyle(table_style)
    table_mae.splitByRow = True
    elements.append(table_mae)

    elements.append(Spacer(1, 8))

    # -------------------------
    # Tabla de MAE
    # -------------------------

    data_responsable = [
        ["NOMBRE RESPONSABLE", "CARGO RESPONSABLE", "CELULAR RESPONSABLE", "CORREO RESPONSABLE"]
    ]
    data_responsable.append([
        str(postulacion.responsable.persona.nombrecompleto()),
        str(postulacion.responsable.persona.cargo),
        str(postulacion.responsable.persona.celular),
        str(postulacion.responsable.correo),
    ])

    data_responsable = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_responsable]
    table_responsable = Table(data_responsable, colWidths=[130, 130, 130, 130], rowHeights=25)
    table_responsable.setStyle(table_style)
    table_responsable.splitByRow = True
    elements.append(table_responsable)
    elements.append(Spacer(1, 10))

    # Título de sección
    subt0 = f"1.- DATOS PRINCIPALES DEL PROYECTO:"
    subt0_title = Paragraph(subt0, style_left)
    elements.append(subt0_title)

    # -------------------------
    # Tabla nombre proyecto 
    # -------------------------
    data_nombre = [
        ["NOMBRE DEL PROYECTO",str(proyecto.nombre)],
        ["BENEFICIARIOS",str(proyecto.comunidades)],
    ]
    data_nombre = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_nombre]
    table_nombre = Table(data_nombre, colWidths=[130, 390], rowHeights=25)
    table_nombre.setStyle(table_style_V)
    table_nombre.splitByRow = True
    elements.append(table_nombre)
    if proyecto.tipologia_proy:
        tipologi = 'Proyecto de Desarrollo Social'
    else:
        tipologi = ''

    data_tipo = [
        ["TIPOLOGIA DEL PROYECTO", str(tipologi), "PERIODO DE EJECUCION", str(proyecto.periodo_ejecu), "FINANCIAMIENTO EDTP", "Sí" if proyecto.solicitud_financ else "No"],
    ]
    data_tipo = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_tipo]
    table_tipo = Table(data_tipo, colWidths=[130, 130, 90, 40, 90, 40], rowHeights=20)
    table_tipo.setStyle(table_style_V)
    table_tipo.splitByRow = True
    elements.append(table_tipo)
    elements.append(Spacer(1, 10))

    # Título de sección
    subt2 = f"2.- JUSTIFICACION DE LA INICIATIVA DEL PROYECTO:"
    subt2_title = Paragraph(subt2, style_left)
    elements.append(subt2_title)

    # -------------------------
    # Tabla justificacion 
    # -------------------------

    data_justificacion = [
        ["El proyecto esta acorde a los principios y derechos establecidos en Constitución Política del Estado ?", "Sí" if justificacion.justificacion1 else "No"],
        ["El proyecto esta acorde a Los lineamientos de la Agenda Patriótica 2025 y la Ley N° 300 Marco de la Madre Tierra y Desarrollo Integral para Vivir Bien ?", "Sí" if justificacion.justificacion2 else "No"],
        ["El Proyecto esta acorde a la normativa del Plan Sectorial de Desarrollo Integral del Ministerio de Medio Ambiente y Agua ?", "Sí" if justificacion.justificacion3 else "No"],
        ["El Proyecto esta acorde a la normativa de la Ley de Autonomías y Descentralización 'ANDRES IBAÑEZ' ? ", "Sí" if justificacion.justificacion4 else "No"],
        ["El Proyecto esta acorde a la normativa de la Ley Forestal ?", "Sí" if justificacion.justificacion5 else "No"],
        ["El Proyecto esta acorde al Plan Territorial de Desarrollo Integral (PTDI) ?", "Sí" if justificacion.justificacion6 else "No"],
        ["El Proyecto está dentro de la normativa de los Planes de Gestión Territorial Comunitaria (PGTC)?", "Sí" if justificacion.justificacion7 else "No"],
    ]
    data_justificacion = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_justificacion]
    table_justificacion = Table(data_justificacion, colWidths=[490, 30], rowHeights=15)
    table_justificacion.setStyle(table_style_V)
    table_justificacion.splitByRow = True
    elements.append(table_justificacion)

    elements.append(Spacer(1, 10))

    # Título de sección
    subt3 = f"3.- IDEA DEL PROYECTO:"
    subt3_title = Paragraph(subt3, style_left)
    elements.append(subt3_title)

    # -------------------------
    # Tabla Idea de proyecto 
    # -------------------------

    data_idea = [
        ["ANTECEDENTES"],
        [str(idea.antecedente)],
        ["DIAGNOSTICO DEL PROYECTO"],
        [str(idea.diagnostico)],
        ["PLANTEAMIENTO DEL PROBLEMA / NECESIDAD A RESOLVER CON EL PROYECTO"],
        [str(idea.planteamiento_problema)],
        ["ACTORES INVOLUCRADOS"],
        [str(idea.actores_involucrados)],
        ["ALTERNATIVA DE SOLUCION 1"],
        [str(idea.alternativa_1)],
        ["ALTERNATIVA DE SOLUCION 2"],
        [str(idea.alternativa_2)],
        ["ALTERNATIVA ELEGIDA"],
        [str(idea.elige_alternativa)],
        ["JUSTIFICACION DE LA ALTERNATIVA ELEGIDA"],
        [str(idea.justificacion_alter)],
        ["OBJETIVO GENERAL DEL PROYECTO"],
        [str(idea.objetivo_general)],
    ]
    data_idea = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_idea]
    table_idea = Table(data_idea, colWidths=[520])
    table_idea.setStyle(table_style_V)
    table_idea.splitByRow = True
    elements.append(table_idea)

    subt4 = f"Objetivos especificos:"
    subt4_title = Paragraph(subt4, style_left)
    elements.append(subt4_title)

    # -------------------------
    # Tabla de MAE
    # -------------------------

    data_objetivo = [
        ["OBJETIVO ESPECIFICO", "COMPONENTE", "SITUACION ACTUAL / LINEA DE BASE", "INDICADOR", "META"]
    ]
    for objetivos in objetivo:
        data_objetivo.append([
            str(objetivos.objetivo),
            str(objetivos.componente),
            str(objetivos.linea_base),
            str(objetivos.indicador),
            str(objetivos.meta),
        ])

    data_objetivo = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_objetivo]
    table_objetivo = Table(data_objetivo, colWidths=[104, 104, 104, 104, 104])
    table_objetivo.setStyle(table_style)
    table_objetivo.splitByRow = True
    elements.append(table_objetivo)
    elements.append(Spacer(1, 10))

    # Título de sección
    subt5 = f"Beneficiarios del Proyecto:"
    subt5_title = Paragraph(subt5, style_left)
    elements.append(subt5_title)

    # -------------------------
    # Tabla Idea de proyecto 
    # -------------------------

    data_beneficio = [
        ["Beneficios esperados del Proyecto (ambiental, social y economico)"],
        [str(idea.beneficios_alter)],
    ]
    data_beneficio = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_beneficio]
    table_beneficio = Table(data_beneficio, colWidths=[520])
    table_beneficio.setStyle(table_style_V)
    table_beneficio.splitByRow = True
    elements.append(table_beneficio)
    elements.append(Spacer(1, 5))

    total_directo = beneficiarios.mujer_directo + beneficiarios.hombre_directo
    total_indirecto = beneficiarios.hombre_indirecto + beneficiarios.mujer_indirecto
    total_hombres = beneficiarios.hombre_directo + beneficiarios.hombre_indirecto
    total_mujeres = beneficiarios.mujer_directo + beneficiarios.mujer_indirecto
    total = total_mujeres + total_hombres
    data_beneficiarios = [
        ["<b>Beneficiarios</b>", "<b>Hombres</b>", "<b>Mujeres</b>", "<b>Total</b>"],
        ["Directos",str(beneficiarios.hombre_directo),str(beneficiarios.mujer_directo),str(total_directo)],
        ["Indirectos",str(beneficiarios.hombre_indirecto),str(beneficiarios.mujer_indirecto),str(total_indirecto)],
        ["Total",str(total_hombres),str(total_mujeres),str(total)],
    ]
    data_beneficiarios = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_beneficiarios]
    table_beneficiarios = Table(data_beneficiarios, colWidths=[130,130,130,130])
    table_beneficiarios.setStyle(table_style_V)
    table_beneficiarios.splitByRow = True
    elements.append(table_beneficiarios)
    elements.append(Spacer(1, 5))

    data_beneficiariosF = [
        ["<b>Beneficiarios</b>", "<b>Total</b>"],
        ["Familias",str(beneficiarios.familia)],
    ]
    data_beneficiariosF = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_beneficiariosF]
    table_beneficiariosF = Table(data_beneficiariosF, colWidths=[130, 390])
    table_beneficiariosF.setStyle(table_style_V)
    table_beneficiariosF.splitByRow = True
    elements.append(table_beneficiariosF)

    elements.append(Spacer(1, 10))

    # Título de sección
    subt6 = f"04.- ITCP - MODELO DE ACTA DE CONOCIMIENTO Y ACEPTACIÓN DEL PROYECTO:"
    subt6_title = Paragraph(subt6, style_left)
    elements.append(subt6_title)

    # -------------------------
    # Tabla Idea de proyecto 
    # -------------------------
   
    data_modelo = [
        ["<b>Tipo y Nombre de Beneficiario</b>", "<b>Acta</b>", "<b>Justificacion</b>"]
    ]
    for modelos in modelo:
        data_modelo.append([
            str(modelos.comunidades),
            str(modelos.si_acta),
            str(modelos.no_acta),
        ])

    data_modelo = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_modelo]
    table_modelo = Table(data_modelo, colWidths=[130,195,195])
    table_modelo.setStyle(table_style)
    table_modelo.splitByRow = True
    elements.append(table_modelo)
    elements.append(Spacer(1, 10))

    # Título de sección
    subt7 = f"05.- ESTADO DE SITUACION LEGAL DEL DERECHO PROPIETARIO DE LOS PREDIOS EN LOS QUE SE IMPLEMENTARA EL PROYECTO"
    subt7_title = Paragraph(subt7, style_left)
    elements.append(subt7_title)

    # -------------------------
    # Tabla Idea de proyecto 
    # -------------------------
   
    data_derecho = [
        ["<b>Descripcion del Derecho Propietario</b>", "<b>Registro del Derecho Propietario</b>", "<b>De no contar con derecho propietario determinar las acciones a realizar y plazo</b>", "<b>Georeferenciacion</b>"]
    ]
    for derechos in derecho:
        data_derecho.append([
            str(derechos.descripcion),
            str(derechos.si_registro),
            str(derechos.no_registro),
            "Z="+str(derechos.zone)+"K " + "\n" + str(derechos.easting) + "m E" + "\n" + str(derechos.northing) + "m N" + "\n",
        ])

    data_derecho = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_derecho]
    table_derecho = Table(data_derecho, colWidths=[130, 130, 130, 130])
    table_derecho.setStyle(table_style)
    table_derecho.splitByRow = True
    elements.append(table_derecho)
    elements.append(Spacer(1, 10))
    
    # Título de sección
    subt8 = f"06.- IDENTIFICACION DE POSIBLES IMPACTOS AMBIENTALES"
    subt8_title = Paragraph(subt8, style_left)
    elements.append(subt8_title)

    # -------------------------
    # Tabla Impacto Ambientales
    # -------------------------

    data_impacto = [
        ["<b>Componente Ambiental</b>","<b>Bosque</b>","<b>Suelo</b>","<b>Agua</b>","<b>Aire</b>","<b>Biodiversidad</b>"],
        ["<b>Nivel</b>",str(impacto.bosque_nivel),str(impacto.suelo_nivel),str(impacto.agua_nivel),str(impacto.aire_nivel),str(impacto.biodiversidad_nivel)],
        ["<b>Temporalidad</b>",str(impacto.bosque_tempo),str(impacto.suelo_tempo),str(impacto.agua_tempo),str(impacto.aire_tempo),str(impacto.biodiversidad_tempo)],
    ]
    data_impacto = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_impacto]
    table_impacto = Table(data_impacto, colWidths=[130, 78, 78, 78, 78, 78])
    table_impacto.setStyle(table_style_V)
    table_impacto.splitByRow = True
    elements.append(table_impacto)
    elements.append(Spacer(1, 10))
    
    # Título de sección
    subt9 = f"07.- IDENTIFICACION DE POSIBLES RIESGOS AMBIENTALES"
    subt9_title = Paragraph(subt9, style_left)
    elements.append(subt9_title)
    
    # -------------------------
    # Tabla Riesgos Ambientales
    # -------------------------
   
    data_riesgo = [
        ["<b>Riesgo</b>", "<b>Nivel</b>"]
    ]
    for riesgos in riesgo:
        data_riesgo.append([
            str(riesgos.riesgo),
            str(riesgos.nivel),
        ])

    data_riesgo = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_riesgo]
    table_riesgo = Table(data_riesgo, colWidths=[260, 260])
    table_riesgo.setStyle(table_style)
    table_riesgo.splitByRow = True
    elements.append(table_riesgo)
    elements.append(Spacer(1, 10))
    
    # Título de sección
    subt9 = f"08.- OTROS ASPECTOS QUE SE CONSIDEREN NECESARIOS, DE ACUERDO A LAS CARACTERISTICAS Y COMPLEJIDAD DEL PROYECTO"
    subt9_title = Paragraph(subt9, style_left)
    elements.append(subt9_title)

    # -------------------------
    # Tabla Detalles Poa
    # -------------------------

    data_poa = [
        ["<b>Detalle</b>"],
        [str(poa.descripcion)],
    ]
    data_poa = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_poa]
    table_poa = Table(data_poa, colWidths=[520])
    table_poa.setStyle(table_style_V)
    table_poa.splitByRow = True
    elements.append(table_poa)
    elements.append(Spacer(1, 10))

    # Título de sección
    subt10 = f"09.- PRESUPUESTO REFERENCIAL"
    subt10_title = Paragraph(subt10, style_left)
    elements.append(subt10_title)

    # Título de sección
    subt11 = f"Elaboración Estudio de Diseño Técnico de Preinversión - EDTP:"
    subt11_title = Paragraph(subt11, style_left)
    elements.append(subt11_title)

    # -------------------------
    # Tabla Presupuesto referencial
    # -------------------------

    data_presupuestoelab = [
        ["<b>FONABOSQUE (Bs.)</b>","<b>SOLICITANTE (Bs.)</b>","<b>TOTAL (Bs.)</b>","<b>FONABOSQUE %</b>","<b>SOLICITANTE %</b>","<b>% TOTAL</b>",],
        [str(presupuesto.elab_fona), str(presupuesto.elab_sol), str(presupuesto.elab_total), str(presupuesto.elab_fona_p), str(presupuesto.elab_sol_p), str(presupuesto.elab_total_p)],
    ]
    data_presupuestoelab = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_presupuestoelab]
    table_presLab = Table(data_presupuestoelab, colWidths=[90, 90, 80, 90, 90, 80])
    table_presLab.setStyle(table_style_V)
    table_presLab.splitByRow = True
    elements.append(table_presLab)
    elements.append(Spacer(1, 5))

    # Título de sección
    subt12 = f"Ejecución Estudio de Diseño Técnico de Preinversión - EDTP:"
    subt12_title = Paragraph(subt12, style_left)
    elements.append(subt12_title)
    # -------------------------
    # Tabla Presupuesto referencial
    # -------------------------

    data_presupuestoejec = [
        ["<b>FONABOSQUE (Bs.)</b>","<b>SOLICITANTE (Bs.)</b>","<b>TOTAL (Bs.)</b>","<b>FONABOSQUE %</b>","<b>SOLICITANTE %</b>","<b>% TOTAL</b>",],
        [str(presupuesto.ejec_fona), str(presupuesto.ejec_sol), str(presupuesto.ejec_total), str(presupuesto.ejec_fona_p), str(presupuesto.ejec_sol_p), str(presupuesto.ejec_total_p)],
    ]
    data_presupuestoejec = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_presupuestoejec]
    table_presEjec = Table(data_presupuestoejec, colWidths=[90, 90, 80, 90, 90, 80])
    table_presEjec.setStyle(table_style_V)
    table_presEjec.splitByRow = True
    elements.append(table_presEjec)
    elements.append(Spacer(1, 10))

    # Título de sección
    subt13 = f"10.- CONCLUCIONES Y RECOMENDACIONES"
    subt13_title = Paragraph(subt13, style_left)
    elements.append(subt13_title)

    # -------------------------
    # Tabla Conclusiones y recomendaciones
    # -------------------------

    data_conclusion = [
        ["<b>CONCLUSIONES</b>"],
        [str(conclusion.conclusion)],
        ["<b>RECOMENDACIONES</b>"],
        [str(conclusion.recomendacion)],
    ]
    data_conclusion = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_conclusion]
    table_conclusion = Table(data_conclusion, colWidths=[520])
    table_conclusion.setStyle(table_style_V)
    table_conclusion.splitByRow = True
    elements.append(table_conclusion)
    elements.append(Spacer(1, 10))
    # Generar el PDF
    doc.build(elements)

    return response