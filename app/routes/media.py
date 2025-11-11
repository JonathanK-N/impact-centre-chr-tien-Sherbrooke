from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

media_bp = Blueprint('media', __name__)

@media_bp.route('/')
@login_required
def list():
    # Pour la démo, on utilise des données statiques
    # Dans une vraie application, ces données viendraient de la base de données
    
    videos = [
        {
            'id': 1,
            'title': 'Culte du Dimanche - Message sur l\'Espoir',
            'description': 'Un message puissant sur l\'espoir en temps difficiles.',
            'youtube_id': 'dQw4w9WgXcQ',  # Exemple d'ID YouTube
            'thumbnail': 'https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
            'duration': '45:30',
            'date': '2024-01-14',
            'speaker': 'Pasteur Jean Dupont',
            'category': 'Culte'
        },
        {
            'id': 2,
            'title': 'Étude Biblique - Les Béatitudes',
            'description': 'Étude approfondie des Béatitudes selon Matthieu 5.',
            'youtube_id': 'dQw4w9WgXcQ',
            'thumbnail': 'https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
            'duration': '32:15',
            'date': '2024-01-10',
            'speaker': 'Pasteur Marie Martin',
            'category': 'Étude Biblique'
        }
    ]
    
    audios = [
        {
            'id': 1,
            'title': 'Podcast - La Foi au Quotidien #12',
            'description': 'Comment vivre sa foi dans le monde professionnel.',
            'file_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
            'duration': '28:45',
            'date': '2024-01-12',
            'speaker': 'Équipe Pastorale',
            'category': 'Podcast'
        },
        {
            'id': 2,
            'title': 'Louange - Compilation Janvier 2024',
            'description': 'Les plus beaux chants de louange du mois.',
            'file_url': '/static/audio/louange-janvier.mp3',
            'duration': '52:30',
            'date': '2024-01-31',
            'speaker': 'Équipe de Louange',
            'category': 'Louange'
        }
    ]
    
    documents = [
        {
            'id': 1,
            'title': 'Guide de Lecture Biblique 2024',
            'description': 'Plan de lecture de la Bible pour toute l\'année.',
            'file_url': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
            'size': '2.3 MB',
            'date': '2024-01-01',
            'category': 'Guide'
        },
        {
            'id': 2,
            'title': 'Bulletin d\'Information - Janvier 2024',
            'description': 'Toutes les nouvelles de notre communauté.',
            'file_url': 'https://www.africau.edu/images/default/sample.pdf',
            'size': '1.8 MB',
            'date': '2024-01-15',
            'category': 'Bulletin'
        }
    ]
    
    return render_template('media/list.html', 
                         videos=videos, 
                         audios=audios, 
                         documents=documents)

@media_bp.route('/video/<int:video_id>')
@login_required
def video(video_id):
    # Données statiques pour la démo
    videos = {
        1: {
            'id': 1,
            'title': 'Culte du Dimanche - Message sur l\'Espoir',
            'description': 'Un message puissant sur l\'espoir en temps difficiles. Dans ce message, nous explorons comment maintenir l\'espoir même dans les moments les plus sombres de notre vie.',
            'youtube_id': 'dQw4w9WgXcQ',
            'duration': '45:30',
            'date': '2024-01-14',
            'speaker': 'Pasteur Jean Dupont',
            'category': 'Culte',
            'scripture': 'Romains 15:13',
            'notes': 'Points clés du message:\n1. L\'espoir vient de Dieu\n2. L\'espoir nous donne la force\n3. L\'espoir se partage'
        },
        2: {
            'id': 2,
            'title': 'Étude Biblique - Les Béatitudes',
            'description': 'Étude approfondie des Béatitudes selon Matthieu 5.',
            'youtube_id': 'dQw4w9WgXcQ',
            'duration': '32:15',
            'date': '2024-01-10',
            'speaker': 'Pasteur Marie Martin',
            'category': 'Étude Biblique',
            'scripture': 'Matthieu 5:1-12',
            'notes': 'Les 8 béatitudes expliquées en détail avec applications pratiques.'
        }
    }
    
    video = videos.get(video_id)
    if not video:
        flash('Vidéo non trouvée.', 'error')
        return redirect(url_for('media.list'))
    
    return render_template('media/video.html', video=video)

@media_bp.route('/audio/<int:audio_id>')
@login_required
def audio(audio_id):
    # Données statiques pour la démo
    audios = {
        1: {
            'id': 1,
            'title': 'Podcast - La Foi au Quotidien #12',
            'description': 'Comment vivre sa foi dans le monde professionnel. Discussion avec des témoignages de membres de notre communauté.',
            'file_url': '/static/audio/podcast-12.mp3',
            'duration': '28:45',
            'date': '2024-01-12',
            'speaker': 'Équipe Pastorale',
            'category': 'Podcast',
            'notes': 'Invités: Marie Tremblay (enseignante), Pierre Gagnon (ingénieur), Sophie Lavoie (infirmière)'
        }
    }
    
    audio = audios.get(audio_id)
    if not audio:
        flash('Audio non trouvé.', 'error')
        return redirect(url_for('media.list'))
    
    return render_template('media/audio.html', audio=audio)
