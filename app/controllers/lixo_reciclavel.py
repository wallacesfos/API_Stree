@jwt_required()
def patch_serie_most_seen(id):
    serie = SeriesModel.query.get(id)
    
    if not serie:
        return {"message": "Serie not found"}, HTTPStatus.NOT_FOUND
    
    serie.views += 1
    
    current_app.db.session.add(serie)
    current_app.db.session.commit()

    
    return {}, HTTPStatus.NO_CONTENT
