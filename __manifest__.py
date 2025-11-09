{
    'name': "Walloniades",
    'version': '1.0',
    'depends': ['base'],
    'author': "Laurent Sancinito",
    'category': 'Extra Tools',
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/walloniades_walloniade_views.xml',
        'views/walloniades_equipe_views.xml',
        'views/walloniades_equipe_instance_views.xml',
        'views/walloniades_type_epreuve_views.xml',
        'views/walloniades_classement_line_views.xml',
        'views/walloniades_classement_general_line_views.xml',
        'views/walloniades_resultat_point_views.xml',
        'views/walloniades_resultat_temps_penalite_views.xml',
        'views/walloniades_resultat_temps_niveau_views.xml',
        'views/walloniades_resultat_temps_positif_negatif_views.xml',
        'views/walloniades_epreuve_instance_views.xml',
        'views/walloniades_epreuve_views.xml',
        'views/walloniades_menus.xml',
        ],
    'assets': {
        'web.assets_backend': [
            'walloniades/static/src/css/style.css',
        ],
    },
}
