# twoDboxplot.py
# based on  https://stackoverflow.com/questions/53849636/draw-a-double-box-plot-chart-2-axes-box-plot-box-plot-correlation-diagram-in

# is imported into SFS_estimator_bias_variance.property

#run as standalone, arguments:
#   name of file with 2Ns estimates generated by SFS_estimator_bias_variance.py 
#   optional  second term, "outliers"  for including outliers in the plot,  default is to exclude them
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np
import sys
import argparse

def boxplot_2d(x,y, ax, color="blue", whis=1.5, includeoutliers = False):
    x = np.array(x)
    y = np.array(y)
    xlimits = [np.percentile(x, q) for q in (25, 50, 75)]
    ylimits = [np.percentile(y, q) for q in (25, 50, 75)]

    ##the box
    box = Rectangle(
        (xlimits[0],ylimits[0]),
        (xlimits[2]-xlimits[0]),
        (ylimits[2]-ylimits[0]),
        ec = "black",
        color=color,
        alpha = 0.3,
        zorder=0
    )
    ax.add_patch(box)

    ##the x median
    vline = Line2D(
        [xlimits[1],xlimits[1]],[ylimits[0],ylimits[2]],
        color = color,
        zorder=1
    )
    ax.add_line(vline)

    ##the y median
    hline = Line2D(
        [xlimits[0],xlimits[2]],[ylimits[1],ylimits[1]],
        color = color,
        zorder=1
    )
    ax.add_line(hline)

    ##the central point
    # ax.plot([xlimits[1]],[ylimits[1]], color = color, marker='o')

    ##the x-whisker
    ##defined as in matplotlib boxplot:
    ##As a float, determines the reach of the whiskers to the beyond the
    ##first and third quartiles. In other words, where IQR is the
    ##interquartile range (Q3-Q1), the upper whisker will extend to
    ##last datum less than Q3 + whis*IQR). Similarly, the lower whisker
    ####will extend to the first datum greater than Q1 - whis*IQR. Beyond
    ##the whiskers, data are considered outliers and are plotted as
    ##individual points. Set this to an unreasonably high value to force
    ##the whiskers to show the min and max values. Alternatively, set this
    ##to an ascending sequence of percentile (e.g., [5, 95]) to set the
    ##whiskers at specific percentiles of the data. Finally, whis can
    ##be the string 'range' to force the whiskers to the min and max of
    ##the data.
    iqr = xlimits[2]-xlimits[0]

    ##left
    left = np.min(x[x > xlimits[0]-whis*iqr])
    whisker_line = Line2D(
        [left, xlimits[0]], [ylimits[1],ylimits[1]],
        color = color,
        zorder = 1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [left, left], [ylimits[0],ylimits[2]],
        color = color,
        zorder = 1
    )
    ax.add_line(whisker_bar)

    ##right
    right = np.max(x[x < xlimits[2]+whis*iqr])
    whisker_line = Line2D(
        [right, xlimits[2]], [ylimits[1],ylimits[1]],
        color = color,
        zorder = 1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [right, right], [ylimits[0],ylimits[2]],
        color = color,
        zorder = 1
    )
    ax.add_line(whisker_bar)

    ##the y-whisker
    iqr = ylimits[2]-ylimits[0]

    ##bottom
    bottom = np.min(y[y > ylimits[0]-whis*iqr])
    whisker_line = Line2D(
        [xlimits[1],xlimits[1]], [bottom, ylimits[0]], 
        color = color,
        zorder = 1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [xlimits[0],xlimits[2]], [bottom, bottom], 
        color = color,
        zorder = 1
    )
    ax.add_line(whisker_bar)

    ##top
    top = np.max(y[y < ylimits[2]+whis*iqr])
    whisker_line = Line2D(
        [xlimits[1],xlimits[1]], [top, ylimits[2]], 
        color = color,
        zorder = 1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [xlimits[0],xlimits[2]], [top, top], 
        color = color,
        zorder = 1
    )
    ax.add_line(whisker_bar)

    ##outliers
    if includeoutliers:
        mask = (x<left)|(x>right)|(y<bottom)|(y>top)
        ax.scatter(
            x[mask],y[mask],
            facecolors='none', edgecolors=color
        )



def make2Dboxplot(alldata,truevals, xparamlabel,yparamlabel,filename,includeoutliers,ylimb=None,ylimt=None,xliml=None,xlimr = None):
    # each data set is a pair of lists 
    # alldata is a list of lists of lists
    #  alldata[0] is the first data set,  alldata[0][0] is the x vals for that data set,  alldata[0][1] is the y vals
    # for example
    #   [
    #     [[1.5,2.1],[5.4,6.3]]  First plot
    #     [[3.4,1.2],[7.8,6.9]]  Second plot
    #   ]
    # truevals is the true values, it is a list of lists
    # for example 
    # [
    #     [1.9,5.2]  First plot
    #     [2.6,7.5]  Second plot
    # ]
    colors = ["red","blue","green","cyan","magenta","black"]
    # fig, ax = plt.subplots()  # a figure with a single Axes
    fig, ax = plt.subplots(figsize=(6, 6))
    n = len(alldata)
    for i in range(n):
        x = alldata[i][0]
        y = alldata[i][1]
        truevalx =float(truevals[i][0])
        truevaly = float(truevals[i][1])
        color = colors[i]
        # print(i,x,y,ax,color)
        boxplot_2d(x,y,ax=ax,color=color, whis=1,includeoutliers = includeoutliers)
        ax.tick_params(axis='both', which='major', labelsize=12)
        plt.plot(truevalx, truevaly, marker="o", markersize=10, markeredgecolor="black", markerfacecolor=color)
    plt.xlabel(xparamlabel,fontsize=14)
    # plt.xlabel(r'$\mu$')
    plt.ylabel(yparamlabel,fontsize=14)
    if ylimb:
        ax.set_ylim(bottome = ylimb)
    else:
        ax.set_ylim(bottom=0)
    if ylimt:
        ax.set_ylim(top=ylimt)
    if xliml:
        ax.set_xlim(left = xliml)
    else:
        ax.set_xlim(left = 0)
    if xlimr:
        ax.set_xlim(right = xlimr)
    # plt.show()    
    plt.savefig(filename)
    return

def parsecommandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",dest="fname",required= True,type=str,help="filename")
    parser.add_argument("-o",dest="includeoutliers",action="store_true",default=False,help="include outliers")
    parser.add_argument("-b",dest="ylimb",default = None,type=float,help="ylim bottom")
    parser.add_argument("-t",dest="ylimt",default = None,type=float,help="ylim top")
    parser.add_argument("-l",dest="xliml",default = None,type=float,help="xlim left")
    parser.add_argument("-r",dest="xlimr",default = None,type=float,help="xlim right")
    args  =  parser.parse_args(sys.argv[1:])  
    args.commandstring = " ".join(sys.argv[1:])
    return args

if __name__ == '__main__':
    """

    """
    args = parsecommandline()
    includeoutliers =  args.includeoutliers
    plotfname = args.fname[:-4] + "_with_outliers_alt2dplot.png" if includeoutliers else args.fname[:-4] + "_alt2dplot.png"
    gf = open(args.fname,'r')
    allgs = []
    truevals = []
    gi = 0
    while True:
        ls = gf.readline().strip().split()
        if len(ls) <= 1:
            break
        truevals.append([float(ls[0])])
        g1s = list(map(float,ls[1:]))
        ls = gf.readline().strip().split()
        truevals[gi].append(float(ls[0]))
        g2s = list(map(float,ls[1:]))
        allgs.append([g1s,g2s])
        gf.readline()
        gi += 1
    gf.close()
    if 'lognormal' in args.fname[:-4].split('_'):
        densitymodel = 'lognormal'
    elif 'gamma' in args.fname[:-4].split('_'):
        densitymodel = 'gamma'
    else:
        densitymodel = 'model'
    if densitymodel =='lognormal':
        make2Dboxplot(allgs,truevals,r'$\mu$',r'$\sigma$',plotfname,includeoutliers,ylimb=args.ylimb,ylimt=args.ylimt,xliml=args.xliml,xlimr=args.xlimr)
    elif densitymodel == "gamma":
        make2Dboxplot(allgs,truevals,r'$\alpha$',r'$\beta$',plotfname,includeoutliers,ylimb=args.ylimb,ylimt=args.ylimt,xliml=args.xliml,xlimr=args.xlimr)



    #some fake data
    # x = np.random.rand(1000)**2
    # y = np.sqrt(np.random.rand(1000))

    # x2 = 0.5+np.random.rand(1000)**2
    # y2 = 0.5+np.sqrt(np.random.rand(1000))

    # alldata = [[x,y],[x2,y2]]
    # truevals = [[0.5**2,0.5**0.5],[0.5+0.5**2,0.5+0.5**0.5]]

    # make2Dboxplot(alldata,truevals,"x string",'y string',"try2dplot.png")
    #x = np.random.rand(1000)
    #y = np.random.rand(1000)

    # #the figure and axes
    # fig,(ax1,ax2) = plt.subplots(ncols=2)

    # #plotting the original data
    # ax1.scatter(x,y,c='r', s=1)

    # #doing the box plot
    # boxplot_2d(x,y,ax=ax2, whis=1)


    # fig, ax = plt.subplots()  # a figure with a single Axes
    # boxplot_2d(x,y,ax=ax, whis=1)
    # boxplot_2d(x2,y2,ax=ax, color="yellow", whis=1)

    # x = 0.5**2
    # y = 0.5** 0.5
    # plt.plot(x, y, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")

    # plt.xlabel("Calorie Burnage")
    # plt.ylabel("Calorie Burnage")
    # plt.show()