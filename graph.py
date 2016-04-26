import rpy2
from rpy2.robjects.packages import importr
#import rpy2.interactive as rinter
import rpy2.robjects as ro
import sys

if len(sys.argv)>4:
    ycar = float(sys.argv[1])
    ycol = int(sys.argv[2])
    ycla = int(sys.argv[3])
    ypri = float(sys.argv[4])

r_base = importr('base')
stats = importr('stats')
graphics = importr('graphics')

labels = "carat,color,clarity,depth,table,sym,pol,price"
print "Opening File"
f = open("output.csv")
lines = f.readlines()
carat = []
color = []
clarity = []
sym = []
pol = []
price = []
for line in lines:
    ls = line.split(",")
    carat.append(ls[2])
    color.append(ls[3])
    clarity.append(ls[4])
    sym.append(ls[7])
    pol.append(ls[8])
    price.append(ls[9])
print "Finished importing the file"

carat = ro.FloatVector(carat)
color = ro.IntVector(color)
clarity = ro.IntVector(clarity)
sym = ro.IntVector(sym)
pol = ro.IntVector(pol)
price = ro.FloatVector(price)
ro.globalenv["carat"] = carat
ro.globalenv["color"] = color
ro.globalenv["clarity"] = clarity
ro.globalenv["sym"] = sym
ro.globalenv["pol"] = pol
ro.globalenv["price"] = price

print "Building Model"
res = stats.lm("price ~ carat + color + clarity")
print "Finished building the model"
print(res)
print "Building prediction"
pred = stats.predict(res)
print "Finished building prediction"
summary = r_base.summary(res)
print "Results from prediction"
print summary
ars = "Adjusted R Squared = " + str(round(summary[8][0],2))
print "Finding Coefficients"
coef = summary.rx2('coefficients')[0:6]
formula = "Price = " + str(int(round(coef[0]))) + " + " + str(int(round(coef[1]))) + "*Carats + " + str(int(round(coef[2]))) + "*Color + " + str(int(round(coef[3]))) + "*Clarity" 
print formula

print "Comparing Actual to Predicted Price Fit"
ro.globalenv["pred"] = pred
comp = stats.lm("pred ~ price")


print "Writing graph to pdf"
ro.r.pdf('prediction.pdf')
ro.r.plot([x for x in pred],[y for y in price], main="Actual vs Predicted Price",xlab="Predicted Price",ylab="Actual Price", cex=0.5)
ro.r.abline(comp,col="green",lty="dotted",lwd=3)

#If purchased diamond, plot it on the graph
if len(sys.argv)>4:
    ypred = coef[0] + coef[1]*ycar + coef[2]*ycol + coef[3]*ycla
    Sdiam = "Your Diamond: " + str(ycar) + " Carats, " + str(ycol) + " Color, " + str(ycla) + " Clarity, $" + str(ypri)
    Spred = "Predicted Price = $" + str(int(round(ypred)))
    Sdiff = "Difference = $" + str(int(ypred-ypri))
    Ssavings = "Savings = " + str(int(round(100*((ypred-ypri)/ypri)))) + "%"
    ro.r.points(ypred,ypri,col="red",pch='x',cex=1)
    ro.r.legend("bottomright",legend=[Sdiam,Spred,Sdiff,Ssavings], bg = "white",cex=0.5)

ro.r.legend("top",legend=[formula,ars,"Sample Size = " + str(len(price))+" Diamonds"], bg = "white")

ro.r('dev.off()')
print "Finished!"

