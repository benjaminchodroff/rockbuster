import rpy2
from rpy2.robjects.packages import importr
import rpy2.interactive as r
r_base = importr('base')
stats = importr('stats')
graphics = importr('graphics')
age = r.IntVector(range(18,30))
height = r.FloatVector([76.1,77,78.1,78.2,78.8,79.7,79.9,81.1,81.2,81.8,82.8,83.5])
rpy2.robjects.globalenv["age"] = age
rpy2.robjects.globalenv["height"] = height
#rpy2.interactive.process_revents.start()
res = stats.lm("height~age")
print(res)
pred = stats.predict(res)
print(pred)
print dict(pred)
print r_base.summary(res)

graphics.plot(age,height)
graphics.abline(res)
raw_input("Press enter when finished\n")
rpy2.interactive.process_revents.stop()
