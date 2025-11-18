import mongoose from 'mongoose';
import bcrypt from 'bcryptjs';

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true,
    minlength: 6
  },
  firstName: {
    type: String,
    required: true,
    trim: true
  },
  lastName: {
    type: String,
    required: true,
    trim: true
  },
  phone: {
    type: String,
    trim: true
  },
  address: {
    type: String,
    trim: true
  },
  birthDate: {
    type: Date
  },
  gender: {
    type: String,
    enum: ['M', 'F', 'Autre']
  },
  maritalStatus: {
    type: String,
    enum: ['Célibataire', 'Marié(e)', 'Divorcé(e)', 'Veuf/Veuve'],
    default: 'Célibataire'
  },
  membershipStatus: {
    type: String,
    enum: ['Nouveau', 'En formation', 'Baptisé', 'Membre officiel'],
    default: 'Nouveau'
  },
  churchRole: {
    type: String,
    trim: true
  },
  role: {
    type: String,
    enum: ['Admin', 'Responsable Département', 'Responsable Famille', 'Membre'],
    default: 'Membre'
  },
  isActive: {
    type: Boolean,
    default: true
  },
  profileImage: {
    type: String
  },
  departments: [{
    departmentId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Department'
    },
    joinedAt: {
      type: Date,
      default: Date.now
    },
    isActive: {
      type: Boolean,
      default: true
    }
  }],
  families: [{
    familyId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'FamilyImpact'
    },
    joinedAt: {
      type: Date,
      default: Date.now
    },
    status: {
      type: String,
      enum: ['Pending', 'Approved', 'Rejected'],
      default: 'Pending'
    },
    isActive: {
      type: Boolean,
      default: true
    }
  }]
}, {
  timestamps: true
});

// Hash password avant sauvegarde
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  try {
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Méthode pour vérifier le mot de passe
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

// Virtual pour le nom complet
userSchema.virtual('fullName').get(function() {
  return `${this.firstName} ${this.lastName}`;
});

// Méthodes utilitaires
userSchema.methods.hasRole = function(role) {
  return this.role === role;
};

userSchema.methods.isAdmin = function() {
  return this.role === 'Admin';
};

userSchema.methods.toJSON = function() {
  const user = this.toObject();
  delete user.password;
  return user;
};

export default mongoose.models.User || mongoose.model('User', userSchema);