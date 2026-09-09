import logging
import sys

from pyprojroot import here


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    """Unterstützt Logger dabei Errors in die Logs zu schreiben
    """
    logging.getLogger().critical(
        "Unbehandelter Fehler hat das Programm beendet:",
        exc_info=(exc_type, exc_value, exc_traceback),
    )


def setup_logging(log_file: str = "logs/logs.log", level: int = logging.INFO) -> None:
    """Logger, der alles in eine Datei schreibt, da das Programm nur selten ausgeführt wird.
    
    Args:
    log_file: Pfad zur logging-Datei aus Sicht von root_logger
    root/logs/logs.log als default
    level: Logginglevel. Info als default
    
    Returns:
    
    Raises:
    
    Examples:
    
    Note:
    Erstellt die angegebene Datei, falls nicht vorhanden.
    """
    log_path = here(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(
        log_path,
        mode="a",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    
    sys.excepthook = handle_uncaught_exception