import mongoose from 'mongoose';

const donationSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  amount: {
    type: Number,
    required: true,
    min: 0
  },
  currency: {
    type: String,
    default: 'CAD',
    enum: ['CAD', 'USD', 'EUR']
  },
  donationType: {
    type: String,
    enum: ['Dîme', 'Offrande', 'Mission', 'Construction', 'Autre'],
    default: 'Dîme'
  },
  purpose: {
    type: String,
    trim: true
  },
  paymentMethod: {
    type: String,
    enum: ['Stripe', 'PayPal', 'Cash', 'Check', 'Transfer'],
    default: 'Stripe'
  },
  paymentId: {
    type: String,
    trim: true
  },
  paymentStatus: {
    type: String,
    enum: ['Pending', 'Completed', 'Failed', 'Refunded'],
    default: 'Pending'
  },
  receiptNumber: {
    type: String,
    unique: true,
    sparse: true
  },
  isTaxDeductible: {
    type: Boolean,
    default: true
  },
  receiptSent: {
    type: Boolean,
    default: false
  },
  receiptSentAt: {
    type: Date
  },
  donationDate: {
    type: Date,
    default: Date.now
  },
  processedAt: {
    type: Date
  },
  notes: {
    type: String,
    trim: true
  },
  isAnonymous: {
    type: Boolean,
    default: false
  },
  stripeData: {
    paymentIntentId: String,
    chargeId: String,
    customerId: String
  }
}, {
  timestamps: true
});

// Index pour recherche et tri
donationSchema.index({ userId: 1, donationDate: -1 });
donationSchema.index({ donationDate: -1 });
donationSchema.index({ paymentStatus: 1 });
donationSchema.index({ receiptNumber: 1 });

// Virtual pour le montant formaté
donationSchema.virtual('formattedAmount').get(function() {
  return `${this.amount.toFixed(2)} ${this.currency}`;
});

// Méthode pour générer le numéro de reçu
donationSchema.methods.generateReceiptNumber = async function() {
  if (this.receiptNumber) return this.receiptNumber;
  
  const year = this.donationDate.getFullYear();
  const count = await this.constructor.countDocuments({
    donationDate: {
      $gte: new Date(year, 0, 1),
      $lt: new Date(year + 1, 0, 1)
    },
    receiptNumber: { $exists: true }
  });
  
  this.receiptNumber = `ICCS-${year}-${String(count + 1).padStart(6, '0')}`;
  return this.receiptNumber;
};

// Méthode pour marquer comme traité
donationSchema.methods.markAsProcessed = function() {
  this.paymentStatus = 'Completed';
  this.processedAt = new Date();
  return this;
};

// Méthode statique pour les statistiques
donationSchema.statics.getYearlyStats = function(year, userId = null) {
  const match = {
    donationDate: {
      $gte: new Date(year, 0, 1),
      $lt: new Date(year + 1, 0, 1)
    },
    paymentStatus: 'Completed'
  };
  
  if (userId) {
    match.userId = new mongoose.Types.ObjectId(userId);
  }
  
  return this.aggregate([
    { $match: match },
    {
      $group: {
        _id: '$donationType',
        totalAmount: { $sum: '$amount' },
        count: { $sum: 1 }
      }
    },
    { $sort: { totalAmount: -1 } }
  ]);
};

export default mongoose.models.Donation || mongoose.model('Donation', donationSchema);