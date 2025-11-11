from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from decimal import Decimal
from datetime import datetime
from app import db
from app.models.donation import Donation

donations_bp = Blueprint('donations', __name__)

@donations_bp.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    if request.method == 'POST':
        amount = Decimal(request.form.get('amount', '0'))
        donation_type = request.form.get('donation_type', 'Dîme')
        purpose = request.form.get('purpose', '')
        is_anonymous = bool(request.form.get('is_anonymous'))
        
        if amount <= 0:
            flash('Le montant doit être supérieur à 0.', 'error')
            return render_template('donations/donate.html')
        
        # Créer le don
        donation = Donation(
            user_id=current_user.id,
            amount=amount,
            donation_type=donation_type,
            purpose=purpose,
            is_anonymous=is_anonymous,
            payment_method='Stripe',  # Par défaut
            payment_status='Pending'
        )
        
        # S'assurer d'avoir une date avant de générer le reçu
        donation.donation_date = datetime.utcnow()
        # Générer le numéro de reçu
        donation.generate_receipt_number()
        
        db.session.add(donation)
        db.session.commit()
        
        # Ici, on intégrerait Stripe pour le paiement réel
        # Pour la démo, on marque le don comme complété
        donation.payment_status = 'Completed'
        donation.processed_at = datetime.utcnow()
        db.session.commit()
        
        flash(f'Merci pour votre don de {donation.formatted_amount}! Votre reçu fiscal sera envoyé par email.', 'success')
        return redirect(url_for('donations.history'))
    
    return render_template('donations/donate.html')

@donations_bp.route('/history')
@login_required
def history():
    donations = Donation.query.filter_by(user_id=current_user.id).order_by(
        db.desc(Donation.donation_date)
    ).all()
    
    # Statistiques
    total_donated = db.session.query(db.func.sum(Donation.amount)).filter_by(
        user_id=current_user.id,
        payment_status='Completed'
    ).scalar() or Decimal('0')
    
    donations_count = len([d for d in donations if d.payment_status == 'Completed'])
    
    # Dons par type
    donations_by_type = {}
    for donation in donations:
        if donation.payment_status == 'Completed':
            if donation.donation_type not in donations_by_type:
                donations_by_type[donation.donation_type] = Decimal('0')
            donations_by_type[donation.donation_type] += donation.amount
    
    stats = {
        'total_donated': total_donated,
        'donations_count': donations_count,
        'donations_by_type': donations_by_type
    }
    
    return render_template('donations/history.html', 
                         donations=donations, 
                         stats=stats)

@donations_bp.route('/receipt/<int:donation_id>')
@login_required
def receipt(donation_id):
    donation = Donation.query.filter_by(
        id=donation_id,
        user_id=current_user.id
    ).first_or_404()
    
    if donation.payment_status != 'Completed':
        flash('Le reçu n\'est disponible que pour les dons complétés.', 'error')
        return redirect(url_for('donations.history'))
    
    return render_template('donations/receipt.html', donation=donation)

@donations_bp.route('/annual-summary/<int:year>')
@login_required
def annual_summary(year):
    donations = Donation.query.filter(
        Donation.user_id == current_user.id,
        Donation.payment_status == 'Completed',
        db.extract('year', Donation.donation_date) == year
    ).order_by(Donation.donation_date).all()
    
    if not donations:
        flash(f'Aucun don trouvé pour l\'année {year}.', 'info')
        return redirect(url_for('donations.history'))
    
    # Calculs pour le résumé annuel
    total_amount = sum(d.amount for d in donations)
    donations_by_month = {}
    donations_by_type = {}
    
    for donation in donations:
        month = donation.donation_date.strftime('%B %Y')
        if month not in donations_by_month:
            donations_by_month[month] = Decimal('0')
        donations_by_month[month] += donation.amount
        
        if donation.donation_type not in donations_by_type:
            donations_by_type[donation.donation_type] = Decimal('0')
        donations_by_type[donation.donation_type] += donation.amount
    
    summary = {
        'year': year,
        'total_amount': total_amount,
        'donations_count': len(donations),
        'donations_by_month': donations_by_month,
        'donations_by_type': donations_by_type,
        'first_donation': donations[0].donation_date,
        'last_donation': donations[-1].donation_date
    }
    
    return render_template('donations/annual_summary.html', 
                         donations=donations, 
                         summary=summary)
