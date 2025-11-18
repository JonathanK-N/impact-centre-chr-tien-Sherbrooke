import { NextResponse } from 'next/server';
import { authenticateRequest } from '../../../../lib/auth.js';

export async function GET(request) {
  try {
    const authResult = await authenticateRequest(request);
    
    if (authResult.error) {
      return NextResponse.json(
        { error: authResult.error },
        { status: authResult.status }
      );
    }

    return NextResponse.json({
      user: authResult.user.toJSON()
    });

  } catch (error) {
    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    );
  }
}