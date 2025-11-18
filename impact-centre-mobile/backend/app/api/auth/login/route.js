import { NextResponse } from 'next/server';
import connectDB from '../../../../lib/mongodb.js';
import User from '../../../../models/User.js';
import { generateToken } from '../../../../lib/auth.js';

export async function POST(request) {
  try {
    await connectDB();
    
    const { email, password } = await request.json();

    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email et mot de passe requis' },
        { status: 400 }
      );
    }

    const user = await User.findOne({ 
      email: email.toLowerCase(),
      isActive: true 
    });

    if (!user || !(await user.comparePassword(password))) {
      return NextResponse.json(
        { error: 'Identifiants invalides' },
        { status: 401 }
      );
    }

    const token = generateToken(user._id);
    const userData = user.toJSON();

    return NextResponse.json({
      message: 'Connexion réussie',
      token,
      user: userData
    });

  } catch (error) {
    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    );
  }
}