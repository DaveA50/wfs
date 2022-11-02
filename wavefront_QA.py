import glob
import logging
import os
import sys
from tkinter.filedialog import askdirectory

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from mpl_toolkits.mplot3d import art3d


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

matplotlib.rcParams['contour.negative_linestyle'] = 'solid'

wave_folder = askdirectory()
try:
    os.chdir(wave_folder)
except OSError as e:
    print(e)
    sys.exit()

lenslets_x = 47
lenslets_y = 35
lenslet_pitch = 0.15
x_offset = np.round((lenslets_x - 1) * lenslet_pitch / 2, 2)
y_offset = np.round((lenslets_y - 1) * lenslet_pitch / 2, 2)
X_dim = np.linspace(-x_offset, x_offset, lenslets_x)
Y_dim = np.linspace(-y_offset, y_offset, lenslets_y)
X, Y = np.meshgrid(X_dim, Y_dim)
roc = []
pupil = 0
pupil_x = 0
pupil_y = 0
zernike_x = np.arange(15)
zernike_keys = ['Piston',
                'Tip y',
                'Tilt x',
                'Astigm.\n+/-45°',
                'Defocus',
                'Astigm.\n0/90°',
                'Trefoil y',
                'Coma x',
                'Coma y',
                'Trefoil x',
                'Tetrafoil y',
                'Astigm. y',
                'Spherical',
                'Astigm. x',
                'Tetrafoil x']

for filename in glob.glob("*.csv"):
    with open(filename, 'r') as csv:
        logger.info(f'Open: {filename}')
        with open("imagej " + filename[:-3] + 'txt', 'w') as imj_outfile:
            with open("Z " + filename[:-3] + 'txt', 'w') as zernike_outfile:
                z = []
                zernike = []
                for i, line in enumerate(csv):
                    if i == 32:
                        line = [x.strip() for x in line.split(',')]
                        pupil = float(line[1])
                    if i == 34:
                        line = [x.strip() for x in line.split(',')]
                        pupil_x = float(line[1])
                    if i == 35:
                        line = [x.strip() for x in line.split(',')]
                        pupil_y = float(line[1])
                    if 44 <= i <= 58:
                        line = [x.strip() for x in line.split(',')]
                        line = [line[0], line[3]]
                        zernike.append(float(line[1]))
                        zernike_outfile.write(', '.join(line) + '\n')
                    if i == 86:
                        line = [x.strip() for x in line.split(',')]
                        current_roc = float(line[1])
                        roc.append(current_roc)
                    if 101 <= i <= 135:
                        line = [x.strip(',') for x in line.split()]
                        z.append([float(x) for x in line[1:]])
                        imj_outfile.write(', '.join(line[1:]) + '\n')
                logger.info(f'Radius of Curvature: {current_roc:.1f}mm')
                logger.info(f'Zernike Coefficient: {zernike}')
                for i in range(len(zernike)):
                    z_name = zernike_keys[i].replace('\n', '')
                    logger.debug(f'{z_name}: {zernike[i]}')

                # Zernike Plot
                fig = plt.figure(1)
                ax = fig.add_subplot(111)
                ax.yaxis.set_minor_locator(AutoMinorLocator(4))
                plt.bar(zernike_x + 0.5, zernike, align='edge')
                plt.xticks(range(1, 16), zernike_keys, rotation=40, size=8)
                plt.xlim([0, 16])
                for i, j in zip(zernike_x, zernike):
                    if j >= 0:
                        plt.annotate(str(j), xy=(i, j), xytext=(13, 2), textcoords='offset points', size=8)
                    elif j < 0:
                        plt.annotate(str(j), xy=(i, j), xytext=(13, -8), textcoords='offset points', size=8)
                plt.xlabel('Zernike Mode')
                plt.ylabel('Coefficient / micron')
                plt.title(f'Zernike {filename[:-4]}')
                plt.savefig(f'Zernike {filename[:-4]}.png')
                plt.show()
                plt.close()

                # 3D Surface Plot
                Z = np.array(z)
                fig = plt.figure(2)
                ax = fig.gca(projection='3d')
                ax.plot_surface(X, Y, Z, rstride=1, cstride=1, linewidth=0.5, alpha=0.9, cmap='jet', antialiased=True)
                ax.view_init(30, 60)

                # Only plot the aperture if it is entirely within the field of view
                if pupil_x + (pupil / 2) < x_offset and \
                        pupil_x - (pupil / 2) > -x_offset and \
                        pupil_y + (pupil / 2) < y_offset and \
                        pupil_y - (pupil / 2) > -y_offset:

                    pupil_contour = plt.Circle((pupil_x, pupil_y), pupil/2,
                                               fill=False, alpha=0.5, edgecolor='Black', linestyle='dashed')
                    pupil_y_0_offset = np.searchsorted(Y_dim, 0)
                    pupil_x_0_offset = np.searchsorted(X_dim, 0 - lenslet_pitch)
                    pupil_y_pos_offset = np.searchsorted(Y_dim, pupil_x + (pupil / 2) - (lenslet_pitch / 2))
                    pupil_y_neg_offset = np.searchsorted(Y_dim, pupil_x - (pupil / 2) - (lenslet_pitch / 2))
                    pupil_x_pos_offset = np.searchsorted(X_dim, pupil_x + (pupil / 2) - (lenslet_pitch / 2))
                    pupil_x_neg_offset = np.searchsorted(X_dim, pupil_x - (pupil / 2) - (lenslet_pitch / 2))
                    pupil_z = 0
                    pupil_z += Z[pupil_y_0_offset][pupil_x_pos_offset]
                    pupil_z += Z[pupil_y_0_offset][pupil_x_neg_offset]
                    pupil_z += Z[pupil_y_pos_offset][pupil_x_0_offset]
                    pupil_z += Z[pupil_y_neg_offset][pupil_x_0_offset]
                    pupil_z /= 4
                    ax.add_patch(pupil_contour)
                    art3d.pathpatch_2d_to_3d(pupil_contour, z=pupil_z, zdir="z")
                plt.xlabel('mm')
                plt.ylabel('mm')
                plt.title(f'Radius of Curvature: {current_roc:.1f} mm')
                plt.savefig(f'Wavefront 3d {filename[:-4]}.png')
                plt.show()
                plt.close()

                # Flat Contour Plot
                pupil_plt = plt.Circle((pupil_x, pupil_y), pupil/2,
                                       fill=False, alpha=0.5, edgecolor='Black', linestyle='dashed')
                fig = plt.figure(3)
                ax = fig.add_subplot(111)
                ax.add_artist(pupil_plt)
                ax.xaxis.set_minor_locator(AutoMinorLocator(10))
                ax.yaxis.set_minor_locator(AutoMinorLocator(10))
                plt.contour(X, Y, Z, colors='black', linewidths=1)
                plt.contourf(X, Y, Z, cmap='jet')
                plt.xlabel('mm')
                plt.ylabel('mm')
                plt.title(f'Radius of Curvature: {current_roc:.1f} mm')
                plt.savefig(f'Wavefront flat {filename[:-4]}.png')
                plt.show()
                plt.close()

sys.exit(0)
