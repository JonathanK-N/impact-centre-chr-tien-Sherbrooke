import mongoose from 'mongoose';

const departmentSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  description: {
    type: String,
    trim: true
  },
  responsibleId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
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
    isActive: {
      type: Boolean,
      default: true
    }
  }],
  color: {
    type: String,
    default: '#007bff'
  },
  icon: {
    type: String,
    default: 'users'
  }
}, {
  timestamps: true
});

// Index pour recherche
departmentSchema.index({ name: 'text', description: 'text' });

// Méthodes utilitaires
departmentSchema.methods.getMembersCount = function() {
  return this.members.filter(member => member.isActive).length;
};

departmentSchema.methods.addMember = function(userId) {
  const existingMember = this.members.find(
    member => member.userId.toString() === userId.toString()
  );
  
  if (existingMember) {
    existingMember.isActive = true;
    return this;
  }
  
  this.members.push({ userId });
  return this;
};

departmentSchema.methods.removeMember = function(userId) {
  const member = this.members.find(
    member => member.userId.toString() === userId.toString()
  );
  
  if (member) {
    member.isActive = false;
  }
  
  return this;
};

export default mongoose.models.Department || mongoose.model('Department', departmentSchema);