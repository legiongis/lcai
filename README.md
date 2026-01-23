# LCAI

[lcai10.legiongis.com](https://lcai10.legiongis.com)

Arches version dependency: dev/6.2.x

## Background

This is an Arches project originally created for the [Lincoln County Archaeological Initiative](https://www.blm.gov/programs/cultural-heritage-and-paleontology/archaeology/what-we-manage/nevada/lincoln-county-archaeological-initiative) as part of their Round 10 funding period. Feldwork performed in 2019 produced a number of different 3d datasets, so this project is both a holding place and public-facing viewer for that content.

## 3d Datasets

Three different types of 3d data are supported in this project. Each one has a graph and custom report which were adapted from [arches-3d](https://github.com/globaldigitalheritage/arches-3d), an Arches v4.4 project.

- Pointclouds
    Point data processed and displayed with [potree](https://potree.org)
- 3d Rock Art Panel
    PLY data processed with [Nexus](http://vcg.isti.cnr.it/nexus/) into NXS
    Report built with [3DHOP](https://www.3dhop.net/)
- Virtual Tour ( panorama environment)
    Multiple 360° images combined using [Panotour](https://www.panotourplugin.com/)
    Report uses an iframe to display the Panotour HTML.

> All of the assets for these datasets are stored on S3 and loaded into the report interface from there.

As much as possible, the original arches-3d reports have been massaged into the current Arches [Resource Report](https://arches.readthedocs.io/en/stable/extensions/resource-reports/) extension paradigm. However, as they require extra JavaScript libraries and multiple templates, they can not be fully extracted into an Arches package just yet.

In order to support asset storage on S3 (and greatly reduce costs without reducing performance), a new "Cloud URL" node was typically added to each graph, and that URL is used to feed the report display.

The graphs, CSV load files, and reference data are stored in the [legiongis/lcai-pkg](https://github.com/legiongis/lcai-pkg) package.

## Credits

The Basin and Range National Monument 3D Documentation Pilot Study team was led by [Architectural Resources Group](https://www.argsf.com). The [Center of Preservation Research](https://www1.ucdenver.edu/centers/center-of-preservation-research) at the University of Colorado, Denver completed the 3D data collection. [G2 Archaeology](http://www.g2archaeology.com/) and the [Nevada Rock Art Foundation](http://www.bradshawfoundation.com/nevada/index.php) selected the sample sites and features, and provided project support. [Legion GIS](https://legiongis.com) led the Arches development with assistance from [Coherit Associates](http://coherit.com) who created the custom front-end design. All work was overseen by the Bureau of Land Management.

The project's source code was based heavily on the [arches-3d](https://github.com/globaldigitalheritage/arches-3d) project built on Arches 4.4 by @veuncent at [Global Digital Heritage](https://globaldigitalheritage.org/). This upgrade to Arches 6 was performed by @mradamcox.

## Dev notes

### Mapbox basemaps

To update a basemap style:

1. Update data in Mapbox as needed (either upload a new file to a tileset or modify an existing dataset)
2. Update the style in Mapbox
  - The app uses the `LCAI-Outdoors` and `Outdoors` styles
3. Save and re-publish the style
4. Download the zip of the style (from the Share menu)
5. Extract all of the files from the zip into the appropriate `pkg/map_layers/mapbox_spec_json/basemaps/` subdirectory.

To deploy in dev, just re-run the initial data setup and the modified map style will be used.

To deploy in production, find the relevant extracted content and place it directly into the Map Source and Map Layer objects using the Django admin.