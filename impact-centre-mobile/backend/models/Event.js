import mongoose from 'mongoose';

const eventSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    trim: true
  },
  description: {
    type: String,
    trim: true
  },
  startDate: {
    type: Date,
    required: true
  },
  endDate: {
    type: Date
  },
  location: {
    type: String,
    trim: true
  },
  address: {
    type: String,
    trim: true
  },
  eventType: {
    type: String,
    enum: ['General', 'Department', 'Family'],
    default: 'General'
  },
  targetDepartmentId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Department'
  },
  targetFamilyId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'FamilyImpact'
  },
  maxParticipants: {
    type: Number
  },
  registrationRequired: {
    type: Boolean,
    default: false
  },
  registrationDeadline: {
    type: Date
  },
  organizerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  isActive: {
    type: Boolean,
    default: true
  },
  isCancelled: {
    type: Boolean,
    default: false
  },
  participants: [{
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true
    },
    registeredAt: {
      type: Date,
      default: Date.now
    },
    status: {
      type: String,
      enum: ['Confirmed', 'Cancelled', 'Waiting'],
      default: 'Confirmed'
    }
  }],
  image: {
    type: String
  },
  color: {
    type: String,
    default: '#28a745'
  }
}, {
  timestamps: true
});

// Index pour recherche et tri
eventSchema.index({ startDate: 1 });
eventSchema.index({ title: 'text', description: 'text' });
eventSchema.index({ eventType: 1, targetDepartmentId: 1 });

// Virtuals
eventSchema.virtual('currentParticipantsCount').get(function() {
  return this.participants.filter(p => p.status === 'Confirmed').length;
});

eventSchema.virtual('availableSpots').get(function() {
  if (!this.maxParticipants) return null;
  return Math.max(0, this.maxParticipants - this.currentParticipantsCount);
});

eventSchema.virtual('isFull').get(function() {
  if (!this.maxParticipants) return false;
  return this.currentParticipantsCount >= this.maxParticipants;
});

// Méthodes
eventSchema.methods.addParticipant = function(userId) {
  const existingParticipant = this.participants.find(
    p => p.userId.toString() === userId.toString()
  );
  
  if (existingParticipant) {
    existingParticipant.status = 'Confirmed';
    return this;
  }
  
  const status = this.isFull ? 'Waiting' : 'Confirmed';
  this.participants.push({ userId, status });
  return this;
};

eventSchema.methods.removeParticipant = function(userId) {
  const participant = this.participants.find(
    p => p.userId.toString() === userId.toString()
  );
  
  if (participant) {
    participant.status = 'Cancelled';
  }
  
  return this;
};

export default mongoose.models.Event || mongoose.model('Event', eventSchema);