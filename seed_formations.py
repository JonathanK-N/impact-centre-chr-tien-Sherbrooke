#!/usr/bin/env python3
"""
Script pour peupler la base de données avec les formations et modules vidéo
"""

from app import create_app, db
from app.models.formation import Formation, FormationModule

def seed_formations():
    app = create_app()
    
    with app.app_context():
        # Supprimer les données existantes
        FormationModule.query.delete()
        Formation.query.delete()
        
        # Formations PCNC
        pcnc_formations = [
            {
                'title': 'PCNC-001 : Découvrir la vision ICC',
                'description': 'Introduction à la vision et aux valeurs d\'Impact Centre Chrétien',
                'category': 'PCNC',
                'code': 'PCNC-001',
                'thumbnail_url': 'https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
                'duration_total': 60,
                'order_index': 1,
                'modules': [
                    {
                        'title': 'Introduction à ICC',
                        'description': 'Découvrez l\'histoire et la vision d\'Impact Centre Chrétien',
                        'video_id': 'dQw4w9WgXcQ',
                        'duration': 15,
                        'order_index': 1
                    },
                    {
                        'title': 'Nos valeurs fondamentales',
                        'description': 'Les 5 valeurs qui guident notre église',
                        'video_id': 'kXYiU_JCYtU',
                        'duration': 18,
                        'order_index': 2
                    },
                    {
                        'title': 'La culture ICC',
                        'description': 'Comment vivre la culture d\'Impact au quotidien',
                        'video_id': '3JZ_D3ELwOQ',
                        'duration': 12,
                        'order_index': 3
                    },
                    {
                        'title': 'Votre place dans la vision',
                        'description': 'Comment contribuer à la mission d\'ICC',
                        'video_id': 'YQHsXMglC9A',
                        'duration': 15,
                        'order_index': 4
                    }
                ]
            },
            {
                'title': 'PCNC-101 : Identité en Christ',
                'description': 'Découvrez qui vous êtes en tant que nouvelle créature en Christ',
                'category': 'PCNC',
                'code': 'PCNC-101',
                'thumbnail_url': 'https://img.youtube.com/vi/kXYiU_JCYtU/maxresdefault.jpg',
                'duration_total': 75,
                'order_index': 2,
                'modules': [
                    {
                        'title': 'Nouvelle créature',
                        'description': 'Comprendre votre nouvelle identité en Christ',
                        'video_id': 'kXYiU_JCYtU',
                        'duration': 20,
                        'order_index': 1
                    },
                    {
                        'title': 'Fils et filles de Dieu',
                        'description': 'Votre position dans la famille de Dieu',
                        'video_id': '3JZ_D3ELwOQ',
                        'duration': 18,
                        'order_index': 2
                    },
                    {
                        'title': 'Marcher dans l\'identité',
                        'description': 'Vivre selon votre nouvelle nature',
                        'video_id': 'YQHsXMglC9A',
                        'duration': 22,
                        'order_index': 3
                    },
                    {
                        'title': 'Témoigner de l\'identité',
                        'description': 'Partager votre transformation',
                        'video_id': 'dQw4w9WgXcQ',
                        'duration': 15,
                        'order_index': 4
                    }
                ]
            },
            {
                'title': 'PCNC-201 : Leadership serviteur',
                'description': 'Développez un cœur de serviteur et des compétences de leadership',
                'category': 'PCNC',
                'code': 'PCNC-201',
                'thumbnail_url': 'https://img.youtube.com/vi/3JZ_D3ELwOQ/maxresdefault.jpg',
                'duration_total': 90,
                'order_index': 3,
                'modules': [
                    {
                        'title': 'Le modèle de Jésus',
                        'description': 'Jésus, le leader serviteur par excellence',
                        'video_id': '3JZ_D3ELwOQ',
                        'duration': 25,
                        'order_index': 1
                    },
                    {
                        'title': 'Servir avant de diriger',
                        'description': 'L\'importance du service dans le leadership',
                        'video_id': 'YQHsXMglC9A',
                        'duration': 20,
                        'order_index': 2
                    },
                    {
                        'title': 'Développer les autres',
                        'description': 'Former et équiper la prochaine génération',
                        'video_id': 'dQw4w9WgXcQ',
                        'duration': 22,
                        'order_index': 3
                    },
                    {
                        'title': 'Leadership en équipe',
                        'description': 'Travailler ensemble pour l\'impact',
                        'video_id': 'kXYiU_JCYtU',
                        'duration': 23,
                        'order_index': 4
                    }
                ]
            }
        ]
        
        # Formation Baptême
        bapteme_formation = {
            'title': 'Parcours Baptême',
            'description': 'Préparez-vous au baptême d\'eau grâce à des capsules simples et des fiches pratiques',
            'category': 'BAPTEME',
            'code': 'BAPT-001',
            'thumbnail_url': 'https://img.youtube.com/vi/YQHsXMglC9A/maxresdefault.jpg',
            'duration_total': 60,
            'order_index': 1,
            'modules': [
                {
                    'title': 'Pourquoi le baptême chrétien ?',
                    'description': 'Comprendre la signification biblique du baptême',
                    'video_id': 'YQHsXMglC9A',
                    'duration': 18,
                    'order_index': 1
                },
                {
                    'title': 'Engagement et témoignage',
                    'description': 'Préparer votre témoignage personnel',
                    'video_id': 'dQw4w9WgXcQ',
                    'duration': 15,
                    'order_index': 2
                },
                {
                    'title': 'La vie après le baptême',
                    'description': 'Grandir dans la foi après le baptême',
                    'video_id': 'kXYiU_JCYtU',
                    'duration': 12,
                    'order_index': 3
                },
                {
                    'title': 'Questions & Réponses',
                    'description': 'Réponses aux questions fréquentes sur le baptême',
                    'video_id': '3JZ_D3ELwOQ',
                    'duration': 15,
                    'order_index': 4
                }
            ]
        }
        
        # Ateliers
        ateliers = [
            {
                'title': 'Atelier Accueil & Hospitalité',
                'description': 'Apprenez à accueillir avec chaleur et créer une atmosphère d\'hospitalité',
                'category': 'ATELIER',
                'code': 'ATL-ACC',
                'thumbnail_url': 'https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
                'duration_total': 45,
                'order_index': 1,
                'modules': [
                    {
                        'title': 'L\'art de l\'accueil',
                        'description': 'Techniques pour un accueil chaleureux',
                        'video_id': 'dQw4w9WgXcQ',
                        'duration': 12,
                        'order_index': 1
                    },
                    {
                        'title': 'Gérer les situations difficiles',
                        'description': 'Comment réagir face aux défis d\'accueil',
                        'video_id': 'kXYiU_JCYtU',
                        'duration': 15,
                        'order_index': 2
                    },
                    {
                        'title': 'Créer une atmosphère',
                        'description': 'L\'importance de l\'environnement d\'accueil',
                        'video_id': '3JZ_D3ELwOQ',
                        'duration': 10,
                        'order_index': 3
                    },
                    {
                        'title': 'Suivi des nouveaux',
                        'description': 'Accompagner les nouveaux membres',
                        'video_id': 'YQHsXMglC9A',
                        'duration': 8,
                        'order_index': 4
                    }
                ]
            },
            {
                'title': 'Atelier Communication & Réseaux',
                'description': 'Maîtrisez les outils de communication et les réseaux sociaux pour l\'église',
                'category': 'ATELIER',
                'code': 'ATL-COM',
                'thumbnail_url': 'https://img.youtube.com/vi/kXYiU_JCYtU/maxresdefault.jpg',
                'duration_total': 50,
                'order_index': 2,
                'modules': [
                    {
                        'title': 'Communication efficace',
                        'description': 'Principes de base de la communication',
                        'video_id': 'kXYiU_JCYtU',
                        'duration': 15,
                        'order_index': 1
                    },
                    {
                        'title': 'Réseaux sociaux pour l\'église',
                        'description': 'Utiliser Facebook, Instagram pour l\'évangélisation',
                        'video_id': '3JZ_D3ELwOQ',
                        'duration': 18,
                        'order_index': 2
                    },
                    {
                        'title': 'Création de contenu',
                        'description': 'Créer du contenu engageant et spirituel',
                        'video_id': 'YQHsXMglC9A',
                        'duration': 12,
                        'order_index': 3
                    },
                    {
                        'title': 'Mesurer l\'impact',
                        'description': 'Analyser et améliorer votre communication',
                        'video_id': 'dQw4w9WgXcQ',
                        'duration': 5,
                        'order_index': 4
                    }
                ]
            },
            {
                'title': 'Atelier Louange & Technique',
                'description': 'Formation technique et spirituelle pour l\'équipe de louange',
                'category': 'ATELIER',
                'code': 'ATL-LOU',
                'thumbnail_url': 'https://img.youtube.com/vi/3JZ_D3ELwOQ/maxresdefault.jpg',
                'duration_total': 65,
                'order_index': 3,
                'modules': [
                    {
                        'title': 'Le cœur du louangeur',
                        'description': 'L\'attitude spirituelle dans la louange',
                        'video_id': '3JZ_D3ELwOQ',
                        'duration': 20,
                        'order_index': 1
                    },
                    {
                        'title': 'Techniques instrumentales',
                        'description': 'Améliorer votre technique musicale',
                        'video_id': 'YQHsXMglC9A',
                        'duration': 18,
                        'order_index': 2
                    },
                    {
                        'title': 'Travail en équipe',
                        'description': 'Jouer ensemble harmonieusement',
                        'video_id': 'dQw4w9WgXcQ',
                        'duration': 15,
                        'order_index': 3
                    },
                    {
                        'title': 'Gestion du son',
                        'description': 'Bases de la sonorisation pour la louange',
                        'video_id': 'kXYiU_JCYtU',
                        'duration': 12,
                        'order_index': 4
                    }
                ]
            }
        ]
        
        # Créer toutes les formations
        all_formations = pcnc_formations + [bapteme_formation] + ateliers
        
        for formation_data in all_formations:
            modules_data = formation_data.pop('modules')
            
            formation = Formation(**formation_data)
            db.session.add(formation)
            db.session.flush()  # Pour obtenir l'ID
            
            for module_data in modules_data:
                module_data['formation_id'] = formation.id
                module_data['video_url'] = f"https://www.youtube.com/watch?v={module_data['video_id']}"
                module_data['thumbnail_url'] = f"https://img.youtube.com/vi/{module_data['video_id']}/mqdefault.jpg"
                
                module = FormationModule(**module_data)
                db.session.add(module)
        
        db.session.commit()
        print("✅ Formations et modules créés avec succès !")
        print(f"📊 {len(all_formations)} formations créées")
        print(f"📹 {sum(len(f.get('modules', [])) for f in all_formations)} modules vidéo ajoutés")

if __name__ == '__main__':
    seed_formations()