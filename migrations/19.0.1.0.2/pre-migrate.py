import logging

_logger = logging.getLogger(__name__)

def migrate(cr,version):
    if not version:
        return
    
    cr.execute("""
        SELECT 1 FROM information_schema.columns
        WHERE table_name='client_retainer' AND column_name='hours_used'
    """)

    if not cr.fetchone():
        _logger.info("client_retainer.hours_used not found, skipping rename")
        return

    cr.execute("""
        ALTER TABLE client_retainer
        RENAME COLUMN hours_used TO hours_consumed
    """)

    _logger.info("Renamed client_retainer.hours_used -> hours_consumed")