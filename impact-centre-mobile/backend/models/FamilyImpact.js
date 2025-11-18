import mongoose from 'mongoose';

const familyImpactSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  description: {
    type: String,
    trim: true
  },
  address: {
    type: String,
    required: true,
    trim: true
  },
  location: {
    type: {
      type: String,
      enum: ['Point'],
      default: 'Point'
    },
    coordinates: {
      type: [Number], // [longitude, latitude]
      index: '2dsphere'
    }
  },
  postalCode: {
    type: String,
    trim: true
  },
  meetingDay: {
    type: String,
    enum: ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
  },
  meetingTime: {
    type: String // Format "19:30"
  },
  responsibleId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  maxCapacity: {
    type: Number,
    default: 15
  },
  isActive: {
    type: Boolean,
    default: true
  },
  members: [{
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true
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
  }],
  image: {
    type: String
  },
  color: {
    type: String,
    default: '#17a2b8'
  }
}, {
  timestamps: true
});

// Index géospatial
familyImpactSchema.index({ location: '2dsphere' });
familyImpactSchema.index({ name: 'text', description: 'text' });

// Virtuals
familyImpactSchema.virtual('currentMembersCount').get(function() {
  return this.members.filter(m => m.isActive && m.status === 'Approved').length;
});

familyImpactSchema.virtual('availableSpots').get(function() {
  return Math.max(0, this.maxCapacity - this.currentMembersCount);
});

familyImpactSchema.virtual('isFull').get(function() {
  return this.currentMembersCount >= this.maxCapacity;
});

// Méthodes
familyImpactSchema.methods.addMember = function(userId, status = 'Pending') {
  const existingMember = this.members.find(
    m => m.userId.toString() === userId.toString()
  );
  
  if (existingMember) {
    existingMember.status = status;
    existingMember.isActive = true;
    return this;
  }
  
  this.members.push({ userId, status });
  return this;
};

familyImpactSchema.methods.approveMember = function(userId) {
  const member = this.members.find(
    m => m.userId.toString() === userId.toString()
  );
  
  if (member) {
    member.status = 'Approved';
  }
  
  return this;
};

familyImpactSchema.methods.removeMember = function(userId) {
  const member = this.members.find(
    m => m.userId.toString() === userId.toString()
  );
  
  if (member) {
    member.isActive = false;
  }
  
  return this;
};

// Méthode statique pour recherche géographique
familyImpactSchema.statics.findNearby = function(longitude, latitude, maxDistance = 10000) {
  return this.find({
    location: {
      $near: {
        $geometry: {
          type: 'Point',
          coordinates: [longitude, latitude]
        },
        $maxDistance: maxDistance
      }
    },
    isActive: true
  });
};

export default mongoose.models.FamilyImpact || mongoose.model('FamilyImpact', familyImpactSchema);