from datetime import datetime
from sqlalchemy import Numeric
from app import db

class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Montant et devise
    amount = db.Column(Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='CAD')
    
    # Type de don
    donation_type = db.Column(db.String(50), default='Dîme')  # 'Dîme', 'Offrande', 'Mission', 'Construction', 'Autre'
    purpose = db.Column(db.String(200))  # Description spécifique du don
    
    # Informations de paiement
    payment_method = db.Column(db.String(50))  # 'Stripe', 'PayPal', 'Cash', 'Check'
    payment_id = db.Column(db.String(100))  # ID de transaction externe
    payment_status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Completed', 'Failed', 'Refunded'
    
    # Reçu fiscal
    receipt_number = db.Column(db.String(50), unique=True)
    is_tax_deductible = db.Column(db.Boolean, default=True)
    receipt_sent = db.Column(db.Boolean, default=False)
    receipt_sent_at = db.Column(db.DateTime)
    
    # Dates
    donation_date = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # Métadonnées
    notes = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', back_populates='donations')
    
    def generate_receipt_number(self):
        """Génère un numéro de reçu unique"""
        if not self.donation_date:
            self.donation_date = datetime.utcnow()
        year = self.donation_date.year
        # Format: ICCS-YYYY-XXXXXX (Impact Centre Chrétien Sherbrooke)
        count = Donation.query.filter(
            db.extract('year', Donation.donation_date) == year
        ).count() + 1
        self.receipt_number = f"ICCS-{year}-{count:06d}"
    
    @property
    def formatted_amount(self):
        return f"{self.amount:.2f} {self.currency}"
    
    def __repr__(self):
        return f'<Donation {self.formatted_amount} by {self.user.full_name}>'
