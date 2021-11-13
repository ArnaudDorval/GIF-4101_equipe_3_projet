
from get_db_data import *
from datetime import date
import matplotlib.pyplot as plt

def main():
    _db = get_db_data()
    data = _db.get_all()

    print(data.head())
    #df.to_csv("test.csv", encoding='utf-8', index=False)

    #fait une liste de differentes description de climat
    weathers = _db.make_weather_desc_list(data)

    # remplace les description climat par la classe recuperer de fct make_weather_desc_list
    new_df = _db.weather_desc_to_int(data)

    #civiere occ/civiere disponible ajoute une colonne CIV_NORMALISE
    new_df = _db.normaliser_valeur_de_civ(new_df)

    #permet de donner la classe str selon l'achalandage
    #for i in new_df.index:
        #print(_db.val_norm_to_class(new_df.loc[i]))
    print(_db.val_norm_to_class(new_df.loc[5]))

    # ajoute une colonne qui associe la valeur normalise a la classe la plus proche
    new_df = _db.convert_civ_norm_closest_class(new_df)

    #rajoute une colonne WEEKDAY_VALUE qui represente le jour de la semaine a partir de [0->lundi,6->dimanche]
    new_df = _db.add_day_of_the_week(new_df)
    print("ok")


if __name__ == "__main__":
    main()
