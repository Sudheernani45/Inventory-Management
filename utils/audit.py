"""
utils/audit.py — helpers for writing audit log entries.
Import and call log_action() from any route after a DB change.
"""

from flask import session, request as _req
from models.db import db
from models.records import AuditLog
from datetime import datetime


def log_action(action: str, module: str, resource: str = '', detail: str = ''):
    """Write one audit-log row.  Safe to call even if session is empty."""
    try:
        user      = session.get('username', 'system')
        user_role = session.get('role', '')
        ip        = _req.remote_addr or ''
        entry = AuditLog(
            timestamp  = datetime.utcnow(),
            user       = user,
            user_role  = user_role,
            action     = action,
            module     = module,
            resource   = resource,
            detail     = detail,
            ip_address = ip,
        )
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        # Never crash the app because of audit logging
        print(f'[AuditLog] Failed to write entry: {e}')
