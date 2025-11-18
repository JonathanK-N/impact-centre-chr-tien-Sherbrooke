import { NextResponse } from 'next/server';
import connectDB from '../../../lib/mongodb.js';
import Department from '../../../models/Department.js';
import { authenticateRequest } from '../../../lib/auth.js';

export async function GET(request) {
  try {
    await connectDB();
    
    const departments = await Department.find({ isActive: true })
      .populate('responsibleId', 'firstName lastName email')
      .sort({ name: 1 });

    return NextResponse.json({ departments });

  } catch (error) {
    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    );
  }
}

export async function POST(request) {
  try {
    const authResult = await authenticateRequest(request);
    
    if (authResult.error) {
      return NextResponse.json(
        { error: authResult.error },
        { status: authResult.status }
      );
    }

    if (!authResult.user.isAdmin()) {
      return NextResponse.json(
        { error: 'Accès non autorisé' },
        { status: 403 }
      );
    }

    await connectDB();
    
    const { name, description, responsibleId, color, icon } = await request.json();

    if (!name) {
      return NextResponse.json(
        { error: 'Le nom du département est requis' },
        { status: 400 }
      );
    }

    const department = new Department({
      name,
      description,
      responsibleId,
      color,
      icon
    });

    await department.save();
    await department.populate('responsibleId', 'firstName lastName email');

    return NextResponse.json({
      message: 'Département créé avec succès',
      department
    }, { status: 201 });

  } catch (error) {
    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    );
  }
}