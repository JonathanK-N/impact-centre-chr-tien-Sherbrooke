from app import create_app, db
from app.models.department import Department

app = create_app()

with app.app_context():
    # Supprimer tous les départements existants
    Department.query.delete()
    
    # Ajouter les nouveaux départements
    departments = [
        "Accueil",
        "Sécurité",
        "Protocol",
        "Le point info",
        "Entretien",
        "Sono",
        "Projection",
        "Communication",
        "L'événementiel",
        "La restauration",
        "Louange",
        "Intégration",
        "Intercession",
        "Impact Junior",
        "Secrétariat",
        "Formation (coordination)",
        "Famille d'impact",
        "ISF"
    ]
    
    for dept_name in departments:
        dept = Department(name=dept_name, description=f"Département {dept_name}")
        db.session.add(dept)
    
    db.session.commit()
    print(f"{len(departments)} departements ajoutes avec succes!")