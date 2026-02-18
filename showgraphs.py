import plotly.express as pex
from dbcreator import create
import json
import plotly

def analytics():
    conn = create()
    cursor = conn.cursor()

    cursor.execute("""SELECT DATE(join_date) AS joinedon, COUNT(*) AS new_users 
                FROM storeData GROUP BY joinedon ORDER BY joinedon""")
    dates = cursor.fetchall()

    days =[str(d[0]) for d in dates]
    count = [d[1] for d in dates]
    print(dates)
    fig = pex.bar(x=days,y=count,labels={"x":"Date","y":"Number of users"},title="New users per day")
    fig.update_layout(template="plotly_white")

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)