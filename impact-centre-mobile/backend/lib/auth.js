import jwt from 'jsonwebtoken';
import User from '../models/User.js';
import connectDB from './mongodb.js';

const JWT_SECRET = process.env.JWT_SECRET || 'fallback-secret';

export function generateToken(userId) {
  return jwt.sign(
    { userId },
    JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
  );
}

export function verifyToken(token) {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    return null;
  }
}

export async function authenticateRequest(request) {
  try {
    const authHeader = request.headers.get('authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return { error: 'Token manquant', status: 401 };
    }

    const token = authHeader.substring(7);
    const decoded = verifyToken(token);
    
    if (!decoded) {
      return { error: 'Token invalide', status: 401 };
    }

    await connectDB();
    const user = await User.findById(decoded.userId);
    
    if (!user || !user.isActive) {
      return { error: 'Utilisateur non trouvé', status: 401 };
    }

    return { user };
  } catch (error) {
    return { error: 'Erreur d\'authentification', status: 500 };
  }
}

export function requireRole(allowedRoles) {
  return (user) => {
    if (!allowedRoles.includes(user.role)) {
      return { error: 'Accès non autorisé', status: 403 };
    }
    return { user };
  };
}

export async function hashPassword(password) {
  const bcrypt = await import('bcryptjs');
  const salt = await bcrypt.genSalt(12);
  return bcrypt.hash(password, salt);
}

export async function comparePassword(password, hashedPassword) {
  const bcrypt = await import('bcryptjs');
  return bcrypt.compare(password, hashedPassword);
}