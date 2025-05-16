"""
Localization support for the prize drawing application.
"""

TRANSLATIONS = {
    "English": {
        "app_title": "Prize Drawing Application",
        "draw_button": "Start Drawing",
        "add_participant": "Add Participant",
        "name_label": "Name",
        "tickets_label": "Number of Tickets",
        "custom_title": "Custom Drawing Title",
        "participants": "Participants",
        "winner": "Winner",
        "congratulations": "Congratulations!",
        "reset": "Reset",
        "save": "Save Participants",
        "load": "Load Participants",
        "language": "Language",
        "probability": "Probability (%)",
        "drawing_in_progress": "Drawing in progress...",
        "no_participants": "Please add participants before drawing",
        "file_saved": "Participants saved to file",
        "file_loaded": "Participants loaded from file",
        "invalid_file": "Invalid file format",
        "upload_file": "Upload participants file",
        "show_statistics": "Show Statistics",
        "hide_statistics": "Hide Statistics",
        "total_tickets": "Total Tickets",
        "drawing_title": "Prize Drawing"
    },
    "中文": {
        "app_title": "抽獎應用",
        "draw_button": "開始抽獎",
        "add_participant": "添加參與者",
        "name_label": "姓名",
        "tickets_label": "抽獎券數量",
        "custom_title": "自定義抽獎標題",
        "participants": "參與者",
        "winner": "得獎者",
        "congratulations": "恭喜！",
        "reset": "重置",
        "save": "保存參與者",
        "load": "加載參與者",
        "language": "語言",
        "probability": "概率 (%)",
        "drawing_in_progress": "抽獎進行中...",
        "no_participants": "請在抽獎前添加參與者",
        "file_saved": "參與者已保存到文件",
        "file_loaded": "已從文件加載參與者",
        "invalid_file": "文件格式無效",
        "upload_file": "上傳參與者文件",
        "show_statistics": "顯示統計信息",
        "hide_statistics": "隱藏統計信息",
        "total_tickets": "總票數",
        "drawing_title": "抽獎"
    },
    "Español": {
        "app_title": "Aplicación de Sorteo",
        "draw_button": "Comenzar Sorteo",
        "add_participant": "Añadir Participante",
        "name_label": "Nombre",
        "tickets_label": "Número de Boletos",
        "custom_title": "Título Personalizado",
        "participants": "Participantes",
        "winner": "Ganador",
        "congratulations": "¡Felicitaciones!",
        "reset": "Reiniciar",
        "save": "Guardar Participantes",
        "load": "Cargar Participantes",
        "language": "Idioma",
        "probability": "Probabilidad (%)",
        "drawing_in_progress": "Sorteo en progreso...",
        "no_participants": "Por favor añade participantes antes del sorteo",
        "file_saved": "Participantes guardados en archivo",
        "file_loaded": "Participantes cargados desde archivo",
        "invalid_file": "Formato de archivo inválido",
        "upload_file": "Subir archivo de participantes",
        "show_statistics": "Mostrar Estadísticas",
        "hide_statistics": "Ocultar Estadísticas",
        "total_tickets": "Total de Boletos",
        "drawing_title": "Sorteo de Premios"
    }
}

def get_text(key, language="English"):
    """Get the localized text for a given key and language."""
    if language not in TRANSLATIONS:
        language = "English"
    return TRANSLATIONS[language].get(key, TRANSLATIONS["English"].get(key, key))

def get_available_languages():
    """Get list of available languages."""
    return list(TRANSLATIONS.keys())
