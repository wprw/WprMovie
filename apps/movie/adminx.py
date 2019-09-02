import xadmin
from movie import models

xadmin.site.register(models.Movie)
xadmin.site.register(models.Comment)
xadmin.site.register(models.Preview)
xadmin.site.register(models.Tag)
xadmin.site.register(models.Moviecol)






