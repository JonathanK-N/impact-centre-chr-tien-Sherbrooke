import { NextResponse } from 'next/server';
import connectDB from '../../../../lib/mongodb.js';
import User from '../../../../models/User.js';
import { generateToken } from '../../../../lib/auth.js';

export async function POST(request) {
  try {
    await connectDB();
    
    const { email, password, firstName, lastName, phone } = await request.json();

    if (!email || !password || !firstName || !lastName) {
      return NextResponse.json(
        { error: 'Tous les champs obligatoires doivent être remplis' },
        { status: 400 }
      );
    }

    if (password.length < 6) {
      return NextResponse.json(
        { error: 'Le mot de passe doit contenir au moins 6 caractères' },
        { status: 400 }
      );
    }

    const existingUser = await User.findOne({ 
      email: email.toLowerCase() 
    });

    if (existingUser) {
      return NextResponse.json(
        { error: 'Cette adresse email est déjà utilisée' },
        { status: 409 }
      );
    }

    const user = new User({
      email: email.toLowerCase(),
      password,
      firstName,
      lastName,
      phone
    });

    await user.save();

    const token = generateToken(user._id);
    const userData = user.toJSON();

    return NextResponse.json({
      message: 'Inscription réussie',
      token,
      user: userData
    }, { status: 201 });

  } catch (error) {
    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    );
  }
}