import os
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from django.utils import timezone
from django.contrib import messages

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from django.db.models import Prefetch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.platypus import Spacer, Image
import qrcode
from io import BytesIO

from solicitud.models import Postulacion

from proyecto.models import (DatosProyectoBase, Justificacion, Idea_Proyecto, Objetivo_especifico, Beneficiario,
                             Modelo_Acta, Derecho_propietario, Impacto_ambiental, Riesgo_desastre, Detalle_POA,
                             Conclusion_recomendacion, Declaracion_jurada, PresupuestoReferencial,
                             Proyecto, ObjetivoGeneralEjec, ObjetivoEspecificoEjec, UbicacionGeografica,
                             EDTP)

from proyecto.forms import R_Declaracion_ITCP, R_Proyecto

   
def generate_pdf(request, slug):
    # Creamos una respuesta HttpResponse para devolver el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="proyecto_detalles_{slug}.pdf"'

    # Crear el objeto SimpleDocTemplate
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    postulacion = Postulacion.objects.get(slug=slug)
    
    # Obtener los objetos Postulacion y DatosProyectoBase usando el slug
    if postulacion.tipo_financiamiento == 1:
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
    else:
        try:
            postulacion = Postulacion.objects.get(slug=slug)
            proyecto = DatosProyectoBase.objects.get(slug=slug)
            beneficiarios = Beneficiario.objects.get(slug=slug)
            declaracion = Declaracion_jurada.objects.get(slug=slug)
            presupuesto = PresupuestoReferencial.objects.get(slug=slug)
            derecho = Derecho_propietario.objects.filter(slug=slug)
            obj_general = ObjetivoGeneralEjec.objects.get(slug=slug)
            obj_especifico = ObjetivoEspecificoEjec.objects.filter(slug=slug)
            ubicacion = UbicacionGeografica.objects.get(slug=slug)            
        except (Postulacion.DoesNotExist, DatosProyectoBase.DoesNotExist, Beneficiario.DoesNotExist, Declaracion_jurada.DoesNotExist,
                PresupuestoReferencial.DoesNotExist, Derecho_propietario.DoesNotExist, ObjetivoGeneralEjec.DoesNotExist, 
                ObjetivoEspecificoEjec.DoesNotExist, UbicacionGeografica.DoesNotExist):
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
    if postulacion.tipo_financiamiento == 1:
        title = f"<u>Informe Técnico de Condiciones Previas</u>"
    else:
        title = f"<u>Estudio de Diseño Técnico de Preinversion</u>"
        
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
    style_lef.alignment = TA_JUSTIFY    # Alineación horizontal centrado (1 = centrado)
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
        ["<b>CODIGO PROYECTO</b>", "<b>DEPARTAMENTO</b>", "<b>ETA</b>", "<b>MUNICIPIO</b>"]
    ]
    data_municipio.append([
        str(postulacion.slug),
        str(postulacion.municipio.departamento),
        str(postulacion.municipio.entidad_territorial),
        str(postulacion.municipio.nombre_municipio),
    ])

    # Convertir cada valor de la tabla en un Paragraph para que el texto se ajuste dentro de las celdas
    data_municipio = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_municipio]
    table_municipio = Table(data_municipio, colWidths=[130, 130, 130, 130])# Crear la tabla
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
        ["<b>NOMBRE MAE</b>", "<b>CARGO MAE</b>", "<b>CELULAR MAE</b>", "<b>CORREO DOMICILIO LEGAL PARA NOTIFICACION</b>"]
    ]
    data_mae.append([
        str(postulacion.mae.persona.nombrecompleto()),
        str(postulacion.mae.persona.cargo),
        str(postulacion.mae.persona.celular),
        str(postulacion.mae.correo),
    ])

    data_mae = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_mae]
    table_mae = Table(data_mae, colWidths=[130, 130, 130, 130])
    table_mae.setStyle(table_style)
    table_mae.splitByRow = True
    elements.append(table_mae)

    elements.append(Spacer(1, 8))

    # -------------------------
    # Tabla de MAE
    # -------------------------

    data_responsable = [
        ["<b>NOMBRE RESPONSABLE</b>", "<b>CARGO RESPONSABLE</b>", "<b>CELULAR RESPONSABLE</b>", "<b>CORREO RESPONSABLE</b>"]
    ]
    data_responsable.append([
        str(postulacion.responsable.persona.nombrecompleto()),
        str(postulacion.responsable.persona.cargo),
        str(postulacion.responsable.persona.celular),
        str(postulacion.responsable.correo),
    ])

    data_responsable = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_responsable]
    table_responsable = Table(data_responsable, colWidths=[130, 130, 130, 130])
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
        ["<b>NOMBRE DEL PROYECTO</b>",str(proyecto.nombre).replace("\n", "<br />")],
        ["<b>BENEFICIARIOS</b>",str(proyecto.comunidades).replace("\n", "<br />")],
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
        ["<b>TIPOLOGIA DEL PROYECTO</b>", str(tipologi), "<b>PERIODO DE EJECUCION (MESES)</b>", str(proyecto.periodo_ejecu).replace("\n", "<br />")],
    ]
    data_tipo = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_tipo]
    table_tipo = Table(data_tipo, colWidths=[130, 130 , 130, 130], rowHeights=20)
    table_tipo.setStyle(table_style_V)
    table_tipo.splitByRow = True
    elements.append(table_tipo)
    elements.append(Spacer(1, 10))
    
    if postulacion.tipo_financiamiento == 1:
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
            ["<b>ANTECEDENTES</b>"],
            [str(idea.antecedente).replace("\n", "<br />")],
            ["<b>DIAGNOSTICO DEL PROYECTO</b>"],
            [str(idea.diagnostico).replace("\n", "<br />")],
            ["<b>PLANTEAMIENTO DEL PROBLEMA / NECESIDAD A RESOLVER CON EL PROYECTO</b>"],
            [str(idea.planteamiento_problema).replace("\n", "<br />")],
            ["<b>ACTORES INVOLUCRADOS</b>"],
            [str(idea.actores_involucrados).replace("\n", "<br />")],
            ["<b>ALTERNATIVA DE SOLUCION 1</b>"],
            [str(idea.alternativa_1).replace("\n", "<br />")],
            ["<b>ALTERNATIVA DE SOLUCION 2</b>"],
            [str(idea.alternativa_2).replace("\n", "<br />")],
            ["<b>ALTERNATIVA ELEGIDA</b>"],
            [str(idea.elige_alternativa)],
            ["<b>JUSTIFICACION DE LA ALTERNATIVA ELEGIDA</b>"],
            [str(idea.justificacion_alter).replace("\n", "<br />")],
            ["<b>OBJETIVO GENERAL DEL PROYECTO</b>"],
            [str(idea.objetivo_general).replace("\n", "<br />")],
        ]
        data_idea = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_idea]
        table_idea = Table(data_idea, colWidths=[520])
        table_idea.setStyle(table_style_V)
        table_idea.splitByRow = True
        elements.append(table_idea)
        
        elements.append(Spacer(1, 10)) 
        subt4 = f"Objetivos especificos:"
        subt4_title = Paragraph(subt4, style_left)
        elements.append(subt4_title)

        # -------------------------
        # Tabla de MAE
        # -------------------------

        data_objetivo = [
            ["<b>OBJETIVO ESPECIFICO</b>", "<b>COMPONENTE</b>", "<b>SITUACION ACTUAL / LINEA DE BASE</b>", "<b>INDICADOR</b>", "<b>META</b>"]
        ]
        for objetivos in objetivo:
            data_objetivo.append([
                str(objetivos.objetivo).replace("\n", "<br />"),
                str(objetivos.componente).replace("\n", "<br />"),
                str(objetivos.linea_base).replace("\n", "<br />"),
                str(objetivos.indicador).replace("\n", "<br />"),
                str(objetivos.meta).replace("\n", "<br />"),
            ])

        data_objetivo = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_objetivo]
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
            ["<b>BENEFICIOS ESPERADOS DEL PROYECTO (AMBIENTAL, SOCIAL Y ECONOMICO)</b>"],
            [str(idea.beneficios_alter).replace("\n", "<br />")],
        ]
        data_beneficio = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_beneficio]
        table_beneficio = Table(data_beneficio, colWidths=[520])
        table_beneficio.setStyle(table_style_V)
        table_beneficio.splitByRow = True
        elements.append(table_beneficio)
        elements.append(Spacer(1, 5))

    else:
        subt2 = f"2.- OBJETIVO:"
        subt2_title = Paragraph(subt2, style_left)
        elements.append(subt2_title)
        
        # Título de sección
        subt3 = f"OBJETIVO GENERAL"
        subt3_title = Paragraph(subt3, style_left)
        elements.append(subt3_title)
        # -------------------------
        # Tabla Objetivo General
        # -
        data_obj_general = [
            ["<b>OBJETIVO GENERAL DEL PROYECTO</b>"],
            [str(obj_general.objetivo_general).replace("\n", "<br />")],
        ]
        data_obj_general = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_obj_general]
        table_obj_general = Table(data_obj_general, colWidths=[520])
        table_obj_general.setStyle(table_style_V)
        table_obj_general.splitByRow = True
        elements.append(table_obj_general)        
        elements.append(Spacer(1, 5)) 
        
        subt4  = f"OBJETIVO ESPECIFICO, COMPONENTES Y METAS:"
        subt4_title = Paragraph(subt4, style_left)
        elements.append(subt4_title)
        
        data_obj_esp = [
            ["<b>OBJETIVO ESPECIFICO</b>", "<b>COMPONENTE</b>", "<b>META</b>"]
        ]
        for objetivos in obj_especifico:
            data_obj_esp.append([
                str(objetivos.objetivo).replace("\n", "<br />"),
                str(objetivos.componente).replace("\n", "<br />"),
                str(objetivos.meta).replace("\n", "<br />"),
            ])

        data_obj_esp = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_obj_esp]
        table_obj_esp = Table(data_obj_esp, colWidths=[174, 173, 173])
        table_obj_esp.setStyle(table_style)
        table_obj_esp.splitByRow = True
        elements.append(table_obj_esp)
        elements.append(Spacer(1, 5))
        # -------------------------
        # Tabla Nro de Hectareas
        # -----------------------
        data_hectarea = [
            ["<b>NÚMERO DE HECTAREAS DE FORESTACIÓN Y/O REFORESTACIÓN Y/O MANEJO SUSTENTABLE DE BOSQUE:</b>", str(obj_general.hectareas).replace("\n", "<br />") + " ha. " + str(obj_general.tipo_hectareas).replace("\n", "<br />")]
        ]
        
        data_hectarea = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_hectarea]
        table_hectarea = Table(data_hectarea, colWidths=[150, 370])
        table_hectarea.setStyle(table_style_V)
        table_hectarea.splitByRow = True
        elements.append(table_hectarea)        
        elements.append(Spacer(1, 10)) 
        
        subt6  = f"03. BENEFICIARIOS"
        subt6_title = Paragraph(subt6, style_left)
        elements.append(subt6_title)
        
    total_directo = beneficiarios.mujer_directo + beneficiarios.hombre_directo
    total_indirecto = beneficiarios.hombre_indirecto + beneficiarios.mujer_indirecto
    total_hombres = beneficiarios.hombre_directo + beneficiarios.hombre_indirecto
    total_mujeres = beneficiarios.mujer_directo + beneficiarios.mujer_indirecto
    total = total_mujeres + total_hombres
    data_beneficiarios = [
        ["<b>Nro Beneficiarios</b>", "<b>Hombres</b>", "<b>Mujeres</b>", "<b>Total</b>"],
        ["<b>Directos</b>",str(beneficiarios.hombre_directo),str(beneficiarios.mujer_directo),str(total_directo)],
        ["<b>Indirectos</b>",str(beneficiarios.hombre_indirecto),str(beneficiarios.mujer_indirecto),str(total_indirecto)],
        ["<b>Total</b>",str(total_hombres),str(total_mujeres),str(total)],
    ]
    data_beneficiarios = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_beneficiarios]
    table_beneficiarios = Table(data_beneficiarios, colWidths=[130,130,130,130])
    table_beneficiarios.setStyle(table_style_V)
    table_beneficiarios.splitByRow = True
    elements.append(table_beneficiarios)
    elements.append(Spacer(1, 5))

    data_beneficiariosF = [
        ["<b>Nro Beneficiarios</b>", "<b>Total</b>"],
        ["<b>Familias</b>",str(beneficiarios.familia)],
    ]
    data_beneficiariosF = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_beneficiariosF]
    table_beneficiariosF = Table(data_beneficiariosF, colWidths=[130, 390])
    table_beneficiariosF.setStyle(table_style_V)
    table_beneficiariosF.splitByRow = True
    elements.append(table_beneficiariosF)

    elements.append(Spacer(1, 10))

    if postulacion.tipo_financiamiento == 1:
        
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
                str(modelos.comunidades).replace("\n", "<br />"),
                str(modelos.si_acta),
                str(modelos.no_acta).replace("\n", "<br />"),
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
                str(derechos.descripcion).replace("\n", "<br />"),
                str(derechos.si_registro),
                str(derechos.no_registro).replace("\n", "<br />"),
                "Z="+str(derechos.zone)+"K " + "\n" + str(derechos.easting) + "m E" + "\n" + str(derechos.northing) + "m N" + "\n",
            ])

        data_derecho = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_derecho]
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
        table_riesgo = Table(data_riesgo, colWidths=[130, 130])
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
            ["<b>DETALLE</b>"],
            [str(poa.descripcion).replace("\n", "<br />")],
        ]
        data_poa = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_poa]
        table_poa = Table(data_poa, colWidths=[520])
        table_poa.setStyle(table_style_V)
        table_poa.splitByRow = True
        elements.append(table_poa)
        elements.append(Spacer(1, 10))
    else:
        subt7  = f"04. UBICACION POSICION GEOGRAFICA:"
        subt7_title = Paragraph(subt7, style_left)
        elements.append(subt7_title)
        
        data_der_prop = [
            ["<b>DESCRIPCION</b>", "<b>ADJUNTAR DERECHO PROPIETARIO</b>", "<b>DE NO CONTAR CON UN DERECHO PROPIETARIO DETERMINAR LAS ACCIONES A REALIZAR</b>", "<b>GEOREFERENCIA (SISTEMA DE REFERENCIA WGS-84 PROYECCION UTM)</b>"]
        ]
        data_der_prop.append([
                str(derecho[0].descripcion).replace("\n", "<br />"),
                str(derecho[0].si_registro),
                str(derecho[0].no_registro).replace("\n", "<br />"),
                "Z="+str(derecho[0].zone)+"K " + "\n" + str(derecho[0].easting) + "m E" + "\n" + str(derecho[0].northing) + "m N" + "\n",
            ])

        data_der_prop = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_der_prop]
        table_der_prop = Table(data_der_prop, colWidths=[130, 130, 130, 130])
        table_der_prop.setStyle(table_style)
        table_der_prop.splitByRow = True
        elements.append(table_der_prop)
        elements.append(Spacer(1, 5))
        
        data_der_prop1 = [
            ["<b>DESCRIPCION</b>", "<b>GEOREFERENCIA (SISTEMA DE REFERENCIA WGS-84 PROYECCION UTM)</b>"]
        ]
        data_der_prop1.append([
                str(derecho[1].descripcion).replace("\n", "<br />"),
                "Z="+str(derecho[1].zone)+"K " + "\n" + str(derecho[1].easting) + "m E" + "\n" + str(derecho[1].northing) + "m N" + "\n",
            ])

        data_der_prop1 = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_der_prop1]
        table_der_prop1 = Table(data_der_prop1, colWidths=[260, 260])
        table_der_prop1.setStyle(table_style)
        table_der_prop1.splitByRow = True
        elements.append(table_der_prop1)
        elements.append(Spacer(1, 5))
        
        data_ubi = [
            ["<b>Altura media zona de forestación</b>", str(ubicacion.alturaForestacion) + " msnm."]
        ]
        
        data_ubi = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_ubi]
        table_ubi = Table(data_ubi, colWidths=[150, 370])
        table_ubi.setStyle(table_style)
        table_ubi.splitByRow = True
        elements.append(table_ubi)
        elements.append(Spacer(1, 5))
    # Título de sección
    if postulacion.tipo_financiamiento == 1:    
        subt10 = f"09.- PRESUPUESTO REFERENCIAL"
    else:
        subt10 = f"05.- COSTO DEL PROYECTO"
        
    subt10_title = Paragraph(subt10, style_left)
    elements.append(subt10_title)
    if postulacion.tipo_financiamiento == 1:
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
        
        subt12 = f"Presupuesto referencial para la Ejecucion del Estudio de Diseño Técnico de Preinversión - EDTP:"

    # Título de sección
    else:
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

    if postulacion.tipo_financiamiento == 1:
            
        # Título de sección
        subt13 = f"10.- CONCLUCIONES Y RECOMENDACIONES"
        subt13_title = Paragraph(subt13, style_left)
        elements.append(subt13_title)

        # -------------------------
        # Tabla Conclusiones y recomendaciones
        # -------------------------

        data_conclusion = [
            ["<b>CONCLUSIONES</b>"],
            [str(conclusion.conclusion).replace("\n", "<br />")],
            ["<b>RECOMENDACIONES</b>"],
            [str(conclusion.recomendacion).replace("\n", "<br />")],
        ]
        data_conclusion = [[Paragraph(str(cell), style_lef) for cell in row] for row in data_conclusion]
        table_conclusion = Table(data_conclusion, colWidths=[520])
        table_conclusion.setStyle(table_style_V)
        table_conclusion.splitByRow = True
        elements.append(table_conclusion)
        elements.append(Spacer(1, 10))

        # Título de sección
        subt14 = f"11.- DECLARACION JURADA"
    else:
        subt14 = f"06.- DECLARACION JURADA"
        
    subt14_title = Paragraph(subt14, style_left)
    elements.append(subt14_title)
    # -------------------------
    # Tabla Declaracion jurada
    # -------------------------
    if postulacion.tipo_financiamiento == 1:
        data_declaracion = [
                ["<b>DECLARACION JURADA</b>"],
                [str(declaracion.declaracion)],
                ["<b>CARTA DE SOLICITUD DE FINANCIAMIENTO PARA ELABORACION DE EDTP</b>"],
                [str(declaracion.carta_elab)],
                ["<b>CARTA DE SOLICITUD DE FINANCIAMIENTO PARA EJECUCION DE EDTP</b>"],
                [str(declaracion.carta_ejec)]
            ]
    else:
        data_declaracion = [
                ["<b>DECLARACION JURADA</b>"],
                [str(declaracion.declaracion)],
                ["<b>CARTA DE SOLICITUD DE FINANCIAMIENTO PARA EJECUCION DE EDTP</b>"],
                [str(declaracion.carta_ejec)]
            ]

    data_declaracion = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_declaracion]
    table_declaracion = Table(data_declaracion, colWidths=[520])
    table_declaracion.setStyle(table_style_V)
    table_declaracion.splitByRow = True
    elements.append(table_declaracion)
    elements.append(Spacer(1, 10))
    data_firma = [
        ["",""],
    ]
    data_firma = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_firma]
    table_firma = Table(data_firma, colWidths=[260,260], rowHeights=70)
    table_firma.setStyle(table_style_V)
    table_firma.splitByRow = True
    elements.append(table_firma)
    data_firmaP = [
        ["<b>Firma y Sello MAE</b>","<b>Firma y Sello TECNICO</b>"],
    ]
    data_firmaP = [[Paragraph(str(cell), style_normal) for cell in row] for row in data_firmaP]
    table_firmaP = Table(data_firmaP, colWidths=[260,260])
    table_firmaP.setStyle(table_style_V)
    table_firmaP.splitByRow = True
    elements.append(table_firmaP)
    elements.append(Spacer(1, 1))
    data = "Convocatoria:"+postulacion.convocatoria.nombre+" Codigo:"+proyecto.slug+", Departamento:"+postulacion.municipio.departamento+", Municipio:"+postulacion.municipio.nombre_municipio
    
    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Crear una imagen del código QR
    img = qr.make_image(fill='black', back_color='white')

    # Guardar la imagen en memoria (sin necesidad de escribir a disco)
    img_io = BytesIO()
    img.save(img_io)
    img_io.seek(0)  # Necesario para leer la imagen desde el inicio

    # Definir tamaño en puntos (3 cm = 85.05 puntos)
    qr_width = 30  # Ancho de la imagen QR en puntos
    qr_height = 30  # Alto de la imagen QR en puntos

    # Insertar la imagen QR en la esquina derecha
    qr_image = Image(img_io)
    qr_image.width = qr_width
    qr_image.height = qr_height
     # Colocar la imagen en la esquina superior derecha
    qr_image.x = 470  # Coordenada X (ajustar según el tamaño de la página)
    qr_image.y = 750  # Coordenada Y (ajustar según el tamaño de la página)


    # Agregar la imagen al documento
    elements.append(qr_image)


    # Otra seccion

    # Generar el PDF
    doc.build(elements)

    return response

class EnviarDatos(View):
    model = Proyecto
    template_name = 'Proyecto/EnviarDatos.html'
    
    def get(self, request, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        declaracion = get_object_or_404(Declaracion_jurada, slug=slug)
        context = {
            'proyecto': proyecto_p,
            'titulo': 'ENVIAR DATOS',
            'entity': 'ENVIAR DATOS',
            'accion': 'ENVIAR',
            'accion2': 'Cancelar',
            'accion2_url': reverse('convocatoria:Index'),
            'error_messages':[]
        }
        
        # Solo agregar el formulario si 'itcp' es None
        if not declaracion.itcp:
            form = R_Declaracion_ITCP()
            context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        error_messages = []
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        declaracion = get_object_or_404(Declaracion_jurada, slug=slug)
        form = R_Declaracion_ITCP(request.POST, request.FILES)  # Recibe los datos POST del formulario
        if form.is_valid():
            itcp_d = form.cleaned_data['itcp']
            tamano_maximo = int(proyecto_p.convocatoria.tamanoDoc)
            if itcp_d:
                if itcp_d.size > tamano_maximo * 1024 * 1024:  # Tamaño máximo en MB
                    error_messages.append('El archivo GENERADO no debe superar los ' + str(proyecto_p.convocatoria.tamanoDoc) + ' MB')
                if not itcp_d.name.endswith('.pdf'):
                    error_messages.append('El archivo GENERADO debe ser en formato PDF.')
            if error_messages:
                proyecto_p = get_object_or_404(Postulacion, slug=slug)
                declaracion = get_object_or_404(Declaracion_jurada, slug=slug)
                context = {
                    'proyecto': proyecto_p,
                    'titulo': 'ENVIAR DATOS',
                    'entity': 'ENVIAR DATOS',
                    'accion': 'ENVIAR',
                    'accion2': 'Cancelar',
                    'accion2_url': reverse('convocatoria:Index'),
                    'error_messages':error_messages,
                }
                if not declaracion.itcp:
                    form = R_Declaracion_ITCP()
                    context['form'] = form
                return render(request, self.template_name, context)
            
            declaracion.itcp = itcp_d            
            declaracion.save()
            if proyecto_p.tipo_financiamiento == 1:                
                Proyecto.objects.create(
                    slug = slug,
                    datos_basicos = get_object_or_404(DatosProyectoBase, slug=slug),
                    justificacion = get_object_or_404(Justificacion, slug=slug),
                    ideaProyecto = get_object_or_404(Idea_Proyecto, slug=slug),
                    beneficiario = get_object_or_404(Beneficiario, slug=slug),
                    impactoAmbiental = get_object_or_404(Impacto_ambiental, slug=slug),
                    detallePoa = get_object_or_404(Detalle_POA, slug=slug),
                    conclusion = get_object_or_404(Conclusion_recomendacion, slug=slug),
                    declaracionJurada = get_object_or_404(Declaracion_jurada, slug=slug),
                    presupuestoRef = get_object_or_404(PresupuestoReferencial, slug=slug),
                    aceptar = False,
                )
            else:
                EDTP.objects.create(
                    slug = slug,
                    datos_basicos = get_object_or_404(DatosProyectoBase, slug=slug),
                    objetivo_gen = get_object_or_404(ObjetivoGeneralEjec, slug=slug),
                    Ubicacion = get_object_or_404(UbicacionGeografica, slug=slug),                    
                    beneficiario = get_object_or_404(Beneficiario, slug=slug),                    
                    presupuestoRef = get_object_or_404(PresupuestoReferencial, slug=slug),                    
                    declaracionJurada = get_object_or_404(Declaracion_jurada, slug=slug),                    
                    aceptar = False,
                )
            messages.success(request, "Los datos se enviaron correctamente.")
            return redirect('convocatoria:Index')
        else:
            messages.error(request, "Hubo un error al enviar los datos.")
            return render(request, self.template_name, {
                'proyecto': proyecto_p,
                'titulo': 'ENVIAR DATOS',
                'entity': 'ENVIAR DATOS',
                'accion': 'ENVIAR',
                'accion2': 'Cancelar',
                'accion2_url': reverse('convocatoria:Index'),
                'form': form,
            })

class enviarDatos2(View):
    model = Proyecto
    template_name = 'Proyecto/EnviarDatos.html'

    def post(self, request, slug):
        proyecto_p = get_object_or_404(Postulacion, slug=slug)
        if proyecto_p.tipo_financiamiento == 1:        
            if not Proyecto.objects.filter(slug=slug).exists():
                Proyecto.objects.create(
                        slug = slug,
                        postulacion = get_object_or_404(Postulacion, slug=slug),
                        datos_basicos = get_object_or_404(DatosProyectoBase, slug=slug),
                        justificacion = get_object_or_404(Justificacion, slug=slug),
                        ideaProyecto = get_object_or_404(Idea_Proyecto, slug=slug),
                        beneficiario = get_object_or_404(Beneficiario, slug=slug),
                        impactoAmbiental = get_object_or_404(Impacto_ambiental, slug=slug),
                        detallePoa = get_object_or_404(Detalle_POA, slug=slug),
                        conclusion = get_object_or_404(Conclusion_recomendacion, slug=slug),
                        declaracionJurada = get_object_or_404(Declaracion_jurada, slug=slug),
                        presupuestoRef = get_object_or_404(PresupuestoReferencial, slug=slug),
                        aceptar = False,

                    )
            else:
                proyecto = Proyecto.objects.get(slug=slug)
                proyecto.estado = 'CORREGIDO'
                proyecto.fecha_actualizacion = timezone.now()
                proyecto.save()
        else:
            if not EDTP.objects.filter(slug=slug).exists():
                EDTP.objects.create(
                    slug = slug,
                    datos_basicos = get_object_or_404(DatosProyectoBase, slug=slug),
                    objetivo_gen = get_object_or_404(ObjetivoGeneralEjec, slug=slug),
                    Ubicacion = get_object_or_404(UbicacionGeografica, slug=slug),                    
                    beneficiario = get_object_or_404(Beneficiario, slug=slug),                    
                    presupuestoRef = get_object_or_404(PresupuestoReferencial, slug=slug),                    
                    declaracionJurada = get_object_or_404(Declaracion_jurada, slug=slug),                    
                    aceptar = False,
                    )
            else:
                proyecto = EDTP.objects.get(slug=slug)
                proyecto.estado = 'CORREGIDO'
                proyecto.fecha_actualizacion = timezone.now()
                proyecto.save()
            # Agregar un mensaje de éxito
        messages.success(request, "Los datos se enviaron correctamente.")
            # Redirigir a la página de éxito o a otro lugar
        return redirect('convocatoria:Index')  # Redirige a la página principal o a la página deseada
       
class verDatos(View):
    model = Proyecto
    template_name = 'Proyecto/Vista.html'

    def get(self, request, slug):        
        postulacion = get_object_or_404(Postulacion, slug=slug)
        derecho = Derecho_propietario.objects.filter(slug=slug)
        
        if postulacion.tipo_financiamiento == 1:            
            proyecto = get_object_or_404(Proyecto, slug=slug)        
            objetivo_esp = Objetivo_especifico.objects.filter(slug=slug)
            modelo_acta = Modelo_Acta.objects.filter(slug=slug)
            riesgo_des = Riesgo_desastre.objects.filter(slug=slug)
            
        else:
            proyecto = get_object_or_404(EDTP, slug=slug)
            objetivo_esp = ObjetivoEspecificoEjec.objects.filter(slug=slug)
            
        total_hombre = int(proyecto.beneficiario.hombre_directo) + int(proyecto.beneficiario.hombre_indirecto)
        total_mujer = int(proyecto.beneficiario.mujer_directo) + int(proyecto.beneficiario.mujer_indirecto)
        total_directo = int(proyecto.beneficiario.hombre_directo) + int(proyecto.beneficiario.mujer_directo)
        total_indirecto = int(proyecto.beneficiario.hombre_indirecto) + int(proyecto.beneficiario.mujer_indirecto)

        p_hombre_dir = round(((100*proyecto.beneficiario.hombre_directo)/total_directo), 2)
        p_mujer_dir = round(((100*proyecto.beneficiario.mujer_directo)/total_directo), 2) 
        p_hombre_indir = round(((100*proyecto.beneficiario.hombre_indirecto)/total_indirecto), 2) 
        p_mujer_indir = round(((100*proyecto.beneficiario.mujer_indirecto)/total_indirecto), 2)
        p_total_dir = p_hombre_dir + p_mujer_dir
        p_total_indir = p_hombre_indir + p_mujer_indir
        
        if self.request.user.is_superuser or self.request.user.is_revisor:
            formulario = True
            form = R_Proyecto(instance = proyecto)
        else: 
            formulario = False
            form = None
            
        context = {
            'proyecto': proyecto,
            'postulacion': postulacion,
            'objetivo': objetivo_esp,
            'derecho' : derecho,
            'titulo': 'DATOS ENVIADOS',
            'entity': 'DATOS ENVIADOS',
            'total_hombre': total_hombre,
            'total_mujer': total_mujer,
            'total_directo': total_directo,
            'total_indirecto': total_indirecto,
            'p_hombre_dir': p_hombre_dir,
            'p_mujer_dir': p_mujer_dir,
            'p_hombre_indir': p_hombre_indir,
            'p_mujer_indir': p_mujer_indir,
            'p_total_dir': p_total_dir,
            'p_total_indir': p_total_indir,
            'vista':True,
            'formulario' : formulario,
            'form' : form,
        }
        
        if postulacion.tipo_financiamiento == 1:
            context.update({                
                'modelo': modelo_acta,
                'derecho': derecho,
                'riesgo': riesgo_des,
            })
            
        return render(self.request, self.template_name, context)
    
    def post(self, request, slug):
        proyecto = Proyecto.objects.get(slug=slug)
        form = R_Proyecto(request.POST, instance = proyecto)
        if form.is_valid():
            datos = form.save(commit=False)
            datos.revisor = self.request.user
            datos.fechaEstado = timezone.now()
            datos.save()
            proyecto = Proyecto.objects.get(slug=slug)
            if proyecto.estado == 'APROBADO':
                proyecto.aceptar = True
                proyecto.fechaEstado = timezone.now()
                proyecto.save()
                messages.success(request, 'Los datos se actualizaron correctamente.')
            return redirect('proyecto:ver_Datos', slug=slug)
        else:
            messages.error(request, 'Hubo un error al actualizar los datos.')
            return self.render_to_response(self.get_context_data(form=form))

class Lista_Proyectos(ListView):
    model = Postulacion
    template_name = 'Proyecto/lista.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_Proyectos, self).get_context_data(**kwargs)
        proyectos = self.model.objects.filter(estado=True).filter(tipo_financiamiento=1)     
        context['titulo'] = 'LISTA DE PROYECTOS CON INICIO DE SESION - ITCP'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS CON INICIO DE SESION - ITCP'
        context['object_list'] = proyectos
                
        return context
    
class Lista_ProyectosEjec(ListView):
    model = Postulacion
    template_name = 'Proyecto/lista.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_ProyectosEjec, self).get_context_data(**kwargs)
        proyectos = self.model.objects.filter(estado=True).filter(tipo_financiamiento=2)
        context['titulo'] = 'LISTA DE PROYECTOS CON INICIO DE SESION - EDTP'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS CON INICIO DE SESION - EDTP'
        context['object_list'] = proyectos
                
        return context
    
class Lista_ProyectosDatos(ListView):
    model = Proyecto
    template_name = 'Proyecto/lista_Datos.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_ProyectosDatos, self).get_context_data(**kwargs)
        # Añadimos el título y la entidad
        context['titulo'] = 'LISTA DE PROYECTOS QUE ENVIARON DATOS'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS QUE ENVIARON DATOS'
        context['object_list'] = Proyecto.objects.all()
                
        return context
    
class Lista_ProyectosDatosEjec(ListView):
    model = EDTP
    template_name = 'Proyecto/lista_Datos.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_ProyectosDatosEjec, self).get_context_data(**kwargs)
        # Añadimos el título y la entidad
        context['titulo'] = 'LISTA DE PROYECTOS QUE ENVIARON DATOS'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS QUE ENVIARON DATOS'
        context['object_list'] = EDTP.objects.all()
                
        return context
    
class Lista_ProyectosSinRevisar(ListView):
    model = Proyecto
    template_name = 'Proyecto/lista_DatosEstado.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_ProyectosSinRevisar, self).get_context_data(**kwargs)
        proyectos = self.model.objects.filter(estado='SIN REVISAR').filter(datos_basicos__postulacion__tipo_financiamiento = 1)
        context['titulo'] = 'LISTA DE PROYECTOS APROBADOS SIN REVISAR'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS APROBADOS SIN REVISAR'
        context['object_list'] = proyectos                
        return context
    
class Lista_ProyectosSinRevisarEjec(ListView):
    model = Proyecto
    template_name = 'Proyecto/lista_DatosEstado.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_ProyectosSinRevisar, self).get_context_data(**kwargs)
        proyectos = self.model.objects.filter(estado='SIN REVISAR').filter(datos_basicos__postulacion__tipo_financiamiento = 2)
        
        # Añadimos el título y la entidad
        context['titulo'] = 'LISTA DE PROYECTOS APROBADOS SIN REVISAR'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS APROBADOS SIN REVISAR'
        context['object_list'] = proyectos
                
        return context
    
class Lista_ProyectosObservados(ListView):
    model = Proyecto
    template_name = 'Proyecto/lista_DatosObservados.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_ProyectosObservados, self).get_context_data(**kwargs)
        revisor = self.request.user
        if self.request.user.is_superuser:
            proyectos = self.model.objects.filter(
                estado__in=['CON OBSERVACION', 'CORREGIDO']
            ).filter(datos_basicos__postulacion__tipo_financiamiento = 1)
        else:
            proyectos = self.model.objects.filter(
                estado__in=['CON OBSERVACION', 'CORREGIDO'],
                revisor=revisor
            ).filter(datos_basicos__postulacion__tipo_financiamiento = 1)
        # Añadimos el título y la entidad
        context['titulo'] = 'LISTA DE PROYECTOS APROBADOS QUE SE OBSERVARON Y/O CORRIGIERON - ITCP'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS APROBADOS QUE SE OBSERVARON Y/O CORRIGIERON - ITCP'
        context['object_list'] = proyectos
                
        return context

class Lista_ProyectosObservadosEjec(ListView):
    model = Proyecto
    template_name = 'Proyecto/lista_DatosObservados.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_ProyectosObservadosEjec, self).get_context_data(**kwargs)
        revisor = self.request.user
        if self.request.user.is_superuser:
            proyectos = self.model.objects.filter(
                estado__in=['CON OBSERVACION', 'CORREGIDO']
            ).filter(datos_basicos__postulacion__tipo_financiamiento = 2)
        else:
            proyectos = self.model.objects.filter(
                estado__in=['CON OBSERVACION', 'CORREGIDO'],
                revisor=revisor
            ).filter(datos_basicos__postulacion__tipo_financiamiento = 2)
        # Añadimos el título y la entidad
        context['titulo'] = 'LISTA DE PROYECTOS APROBADOS QUE SE OBSERVARON Y/O CORRIGIERON - EDTP'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS APROBADOS QUE SE OBSERVARON Y/O CORRIGIERON - EDTP'
        context['object_list'] = proyectos
                
        return context
    
    
class Lista_ProyectosAprobados(ListView):
    model = Proyecto
    template_name = 'Proyecto/lista_DatosEstado.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_ProyectosAprobados, self).get_context_data(**kwargs)
        revisor = self.request.user
        if self.request.user.is_superuser:
            proyectos = self.model.objects.filter(estado='APROBADO').filter(datos_basicos__postulacion__tipo_financiamiento = 1)
        else:
            proyectos = self.model.objects.filter(estado='APROBADO').filter(revisor=revisor).filter(datos_basicos__postulacion__tipo_financiamiento = 1)
        # Añadimos el título y la entidad
        context['titulo'] = 'LISTA DE PROYECTOS APROBADOS QUE NO TIENEN OBSERVACION - ITCP'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS APROBADOS QUE NO TIENEN OBSERVACION - ITCP'
        context['object_list'] = proyectos
                
        return context

   
class Lista_ProyectosAprobadosEJEC(ListView):
    model = Proyecto
    template_name = 'Proyecto/lista_DatosEstado.html'
    def get_context_data(self, **kwargs):
        context = super(Lista_ProyectosAprobadosEJEC, self).get_context_data(**kwargs)
        revisor = self.request.user
        if self.request.user.is_superuser:
            proyectos = self.model.objects.filter(estado='APROBADO').filter(datos_basicos__postulacion__tipo_financiamiento = 2)
        else:
            proyectos = self.model.objects.filter(estado='APROBADO').filter(revisor=revisor).filter(datos_basicos__postulacion__tipo_financiamiento = 2)
        # Añadimos el título y la entidad
        context['titulo'] = 'LISTA DE PROYECTOS APROBADOS QUE NO TIENEN OBSERVACION - EDTP'
        context['activate'] = True
        context['entity'] = 'LISTA DE PROYECTOS APROBADOS QUE NO TIENEN OBSERVACION - EDTP'
        context['object_list'] = proyectos
                
        return context