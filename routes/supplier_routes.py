"""
supplier_routes.py
──────────────────
Token-based Purchase Order approval / rejection for external suppliers.
These routes are PUBLIC (no login required) — suppliers click links from emails.

Endpoints:
  GET  /supplier/approve/<token>          — approve PO
  GET  /supplier/reject/<token>           — show rejection form
  POST /supplier/reject/<token>           — submit rejection reason
"""

from flask import Blueprint, request, jsonify, render_template_string
from models.db import db
from models.records import PurchaseOrder
from datetime import datetime as _dt

supplier_bp = Blueprint('supplier', __name__, url_prefix='/supplier')


# ── Shared page renderer ──────────────────────────────────
def _render_page(icon, heading, body_text, detail_text, header_color, po_number=''):
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ heading }}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', Arial, sans-serif; background: #F1F5F9;
           display: flex; align-items: center; justify-content: center;
           min-height: 100vh; padding: 24px; }
    .card { background: #fff; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,.12);
            max-width: 480px; width: 100%; overflow: hidden; }
    .header { background: {{ header_color }}; padding: 32px 24px; text-align: center; }
    .header .icon { font-size: 56px; line-height: 1; }
    .header h1 { color: #fff; font-size: 24px; margin-top: 12px; font-weight: 700; }
    .body { padding: 28px 32px; }
    .body p { color: #475569; font-size: 15px; line-height: 1.6; margin-bottom: 10px; }
    .po-badge { display: inline-block; background: #EEF2FF; color: #3730A3;
                border-radius: 8px; padding: 6px 16px; font-weight: 700;
                font-size: 15px; margin: 12px 0; letter-spacing: .5px; }
    .footer { border-top: 1px solid #E2E8F0; padding: 16px 32px;
              text-align: center; color: #94A3B8; font-size: 13px; }
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="icon">{{ icon }}</div>
      <h1>{{ heading }}</h1>
    </div>
    <div class="body">
      {% if po_number %}<div class="po-badge">PO # {{ po_number }}</div>{% endif %}
      <p>{{ body_text }}</p>
      <p>{{ detail_text }}</p>
    </div>
    <div class="footer">INVEXA &mdash; Automated Notification</div>
  </div>
</body>
</html>
""", icon=icon, heading=heading, header_color=header_color,
     po_number=po_number, body_text=body_text, detail_text=detail_text)


# ── Approve PO ────────────────────────────────────────────
@supplier_bp.route('/approve/<token>', methods=['GET'])
def supplier_approve_po(token: str):
    po = PurchaseOrder.query.filter_by(supplier_approval_token=token).first()

    if not po:
        return _render_page(
            '❌', 'Invalid Link',
            'This approval link is not valid.',
            'Please contact your account manager if you believe this is an error.',
            '#DC2626'
        ), 404

    if po.supplier_token_expiry and po.supplier_token_expiry < _dt.utcnow():
        return _render_page(
            '⏰', 'Link Expired',
            f'The approval link for PO {po.po_number} has expired.',
            'Please ask the purchasing team to resend a new approval request.',
            '#D97706',
            po.po_number
        ), 410

    if po.supplier_action in ('approved', 'rejected'):
        action_word = 'approved' if po.supplier_action == 'approved' else 'rejected'
        return _render_page(
            '✅' if po.supplier_action == 'approved' else '❌',
            'Already Actioned',
            f'This purchase order has already been {action_word}.',
            'No further action is required.',
            '#2563EB',
            po.po_number
        )

    po.supplier_action      = 'approved'
    po.supplier_actioned_at = _dt.utcnow()
    po.status               = 'Pending'   # moves to Pending for internal approval
    db.session.commit()

    return _render_page(
        '✅', 'Purchase Order Approved',
        f'Thank you! You have successfully approved Purchase Order {po.po_number}.',
        'The purchasing team has been notified and will process your order shortly.',
        '#16A34A',
        po.po_number
    )


# ── Reject PO (GET = form, POST = submit) ─────────────────
_REJECT_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Reject Purchase Order</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', Arial, sans-serif; background: #F1F5F9;
           display: flex; align-items: center; justify-content: center;
           min-height: 100vh; padding: 24px; }
    .card { background: #fff; border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,.12);
            max-width: 480px; width: 100%; overflow: hidden; }
    .header { background: #DC2626; padding: 28px 24px; text-align: center; }
    .header .icon { font-size: 48px; }
    .header h1 { color: #fff; font-size: 22px; margin-top: 10px; font-weight: 700; }
    .body { padding: 28px 32px; }
    .po-badge { display: inline-block; background: #FEE2E2; color: #991B1B;
                border-radius: 8px; padding: 5px 14px; font-weight: 700;
                font-size: 14px; margin-bottom: 16px; }
    label { display: block; font-size: 14px; font-weight: 600;
            color: #374151; margin-bottom: 6px; }
    textarea { width: 100%; padding: 12px; border: 1.5px solid #CBD5E1;
               border-radius: 8px; font-size: 14px; min-height: 120px;
               resize: vertical; outline: none; transition: border-color .2s; }
    textarea:focus { border-color: #DC2626; }
    button { margin-top: 16px; width: 100%; background: #DC2626; color: #fff;
             border: none; padding: 13px; border-radius: 8px; font-size: 15px;
             font-weight: 600; cursor: pointer; transition: background .2s; }
    button:hover { background: #B91C1C; }
    .footer { border-top: 1px solid #E2E8F0; padding: 14px 32px;
              text-align: center; color: #94A3B8; font-size: 12px; }
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="icon">⛔</div>
      <h1>Reject Purchase Order</h1>
    </div>
    <div class="body">
      <div class="po-badge">PO # {{ po_number }}</div>
      <label for="reason">Please provide a reason for rejection:</label>
      <form method="POST">
        <textarea id="reason" name="rejection_reason"
                  placeholder="e.g. Pricing not agreed, product unavailable, delivery timeline not feasible…"
                  required></textarea>
        <button type="submit">Submit Rejection</button>
      </form>
    </div>
    <div class="footer">INVEXA &mdash; Automated Notification</div>
  </div>
</body>
</html>
"""

@supplier_bp.route('/reject/<token>', methods=['GET', 'POST'])
def supplier_reject_po(token: str):
    po = PurchaseOrder.query.filter_by(supplier_approval_token=token).first()

    if not po:
        return _render_page(
            '❌', 'Invalid Link',
            'This rejection link is not valid.',
            'Please contact your account manager if you believe this is an error.',
            '#DC2626'
        ), 404

    if po.supplier_token_expiry and po.supplier_token_expiry < _dt.utcnow():
        return _render_page(
            '⏰', 'Link Expired',
            f'The rejection link for PO {po.po_number} has expired.',
            'Please ask the purchasing team to resend a new approval request.',
            '#D97706',
            po.po_number
        ), 410

    if po.supplier_action in ('approved', 'rejected'):
        return _render_page(
            '✅' if po.supplier_action == 'approved' else '❌',
            'Already Actioned',
            f'This purchase order has already been {po.supplier_action}.',
            'No further action is required.',
            '#2563EB',
            po.po_number
        )

    if request.method == 'GET':
        return render_template_string(_REJECT_FORM, po_number=po.po_number)

    # POST — process the form
    reason = (request.form.get('rejection_reason') or '').strip()
    if not reason:
        return render_template_string(_REJECT_FORM, po_number=po.po_number)

    po.supplier_action         = 'rejected'
    po.supplier_actioned_at    = _dt.utcnow()
    po.supplier_reject_reason  = reason
    po.rejection_reason        = reason
    po.status                  = 'Draft'     # returns to draft for revision
    db.session.commit()

    return _render_page(
        '⛔', 'Purchase Order Rejected',
        f'You have rejected Purchase Order {po.po_number}.',
        f'Reason recorded: "{reason}". The purchasing team has been notified.',
        '#DC2626',
        po.po_number
    )
