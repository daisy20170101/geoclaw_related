
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


#--------------------------
def setplot(plotdata=None):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 


    from clawpack.visclaw import colormaps, geoplot
    from clawpack.visclaw.data import ClawPlotData

    from numpy import linspace

    if plotdata is None:
        plotdata = ClawPlotData()

    plotdata.clearfigures()  # clear any old figures,axes,items data


    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def fixup(current_data):
        import pylab
        t = current_data.t
        hours = int(t//3600)
        minutes = (t-hours*3600)/60
        if hours==0:
            time_string = '    '
        else:
            time_string = '%d h ' %(hours)
        time_string = time_string + '%d min' %(minutes)

        pylab.title('')#'Surface at %4.2f hours' % t, fontsize=15)
        pylab.xticks(fontsize=15)
        pylab.yticks(fontsize=15)
        pylab.xticks(ticks = np.arange(176, 230, 10), labels=[])
        pylab.yticks(ticks = np.arange(30, 67, 10), labels=[])
        pylab.grid(True)

        #add colorbar
        fig = pylab.gcf()
        ax = pylab.gca()
        a = np.array([[-0.1, 0.1]])

        from cmcrameri import cm
        img = pylab.imshow(a, cmap=geoplot.tsunami_colormap)
        cax = fig.add_axes([0.17, 0.5, 0.01, 0.20])
        cb = pylab.colorbar(cax=cax, ticks=np.linspace(-0.1, 0.1, 5))
        cb.ax.tick_params(which='major', labelsize=15, length=8, width =1, direction='out')
        cb.ax.tick_params(which = 'minor', length = 6, width =1.0)
        pylab.sca(ax)
        pylab.text(177, 60, 'ssha (m)', va="top", family="sans-serif",  clip_on=True, fontsize=15, zorder=6, rotation='vertical')
        ax.tick_params(direction='in')
        for tic in ax.xaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
        for tic in ax.yaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False



        #plot Jason location
        import pyproj
        lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
        myproj=pyproj.Proj('EPSG:5936')
#        Jason = np.genfromtxt('./dart_sta.csv', delimiter=",", skip_header=1)
#        xyz = pyproj.transform(myproj, lla, Jason[:,0],Jason[:,1], radians=False)
#        pylab.plot(Jason[:,0], Jason[:,1], color='k', linewidth=2)
       
    #-----------------------------------------
    # Figure for surface
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=0)
    plotfigure.kwargs = {'figsize':[7.5*1.5*30./35.,7.5*1.5], 'facecolor': 'white'}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.scaled = True
    plotaxes.afteraxes = fixup

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.surface
    from cmcrameri import cm    
    plotitem.pcolor_cmap = geoplot.tsunami_colormap
    plotitem.pcolor_cmin = -0.1
    plotitem.pcolor_cmax = 0.1
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0,0]
    plotitem.patchedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land

    from matplotlib import cm as cm1
    from clawpack.visclaw import colormaps
    navajowhite = colormaps.make_colormap({0.:'navajowhite', 1.:'navajowhite'})
    plotitem.pcolor_cmap = navajowhite
    plotitem.pcolor_cmin = 0.
    plotitem.pcolor_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0,0]
    plotitem.patchedges_show = 0
    plotaxes.xlimits = [176,230]
    plotaxes.ylimits = [30,67]

    # Add dashed contour line for shoreline
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0.]
    plotitem.amr_contour_colors = ['k']  # color on each level
    plotitem.amr_contour_show = [1]  # show contours only on finest level
    plotitem.kwargs = {'linewidths': 1}


    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface at gauges', figno=300, \
                    type='each_gauge')
    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Surface'

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

    def add_zeroline(current_data):
        from pylab import plot, legend, xticks, floor, axis, xlabel
        t = current_data.t 
        gaugeno = current_data.gaugeno

        plot(t, 0*t, 'k')
        n = int(floor(t.max()/3600.) + 2)
        xticks([3600*i for i in range(n)], ['%i' % i for i in range(n)])
        xlabel('time (hours)')

    plotaxes.afteraxes = add_zeroline
    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.parallel = True
#    plotdata.print_framenos = [0,5,10,20,30,40,50,60,70,80,90,100,110,120]          # list of frames to print
    plotdata.print_framenos = 'all'
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata
