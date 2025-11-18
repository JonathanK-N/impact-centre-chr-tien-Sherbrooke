import { NextResponse } from 'next/server';
import connectDB from '../../../lib/mongodb.js';
import Event from '../../../models/Event.js';
import { authenticateRequest } from '../../../lib/auth.js';

export async function GET(request) {
  try {
    await connectDB();
    
    const { searchParams } = new URL(request.url);
    const startDate = searchParams.get('startDate');
    const endDate = searchParams.get('endDate');
    const eventType = searchParams.get('eventType');
    
    let query = { isActive: true, isCancelled: false };
    
    if (startDate && endDate) {
      query.startDate = {
        $gte: new Date(startDate),
        $lte: new Date(endDate)
      };
    }
    
    if (eventType && eventType !== 'all') {
      query.eventType = eventType;
    }

    const events = await Event.find(query)
      .populate('organizerId', 'firstName lastName')
      .populate('targetDepartmentId', 'name')
      .populate('targetFamilyId', 'name')
      .sort({ startDate: 1 });

    return NextResponse.json({ events });

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

    await connectDB();
    
    const eventData = await request.json();
    
    if (!eventData.title || !eventData.startDate) {
      return NextResponse.json(
        { error: 'Titre et date de début requis' },
        { status: 400 }
      );
    }

    const event = new Event({
      ...eventData,
      organizerId: authResult.user._id
    });

    await event.save();
    await event.populate([
      { path: 'organizerId', select: 'firstName lastName' },
      { path: 'targetDepartmentId', select: 'name' },
      { path: 'targetFamilyId', select: 'name' }
    ]);

    return NextResponse.json({
      message: 'Événement créé avec succès',
      event
    }, { status: 201 });

  } catch (error) {
    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    );
  }
}