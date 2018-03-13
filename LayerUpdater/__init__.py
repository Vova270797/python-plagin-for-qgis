# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LayerUpdater
                                 A QGIS plugin
 Layer updater
                             -------------------
        begin                : 2017-09-08
        copyright            : (C) 2017 by Vitaliy Prozur/Oleksiy Bondar
        email                : .
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load LayerUpdater class from file LayerUpdater.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .LayerUpdater import LayerUpdater
    return LayerUpdater(iface)
