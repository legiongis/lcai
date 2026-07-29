import ko from 'knockout';
import ReportViewModel from 'viewmodels/report';
import template from 'templates/views/report-templates/iframe-header.htm';

const viewModel = function(params) {
    params.configKeys = [];
    ReportViewModel.apply(this, [params]);

    const srcUrl = this.report?.report_json?.resource["3D Model File"][0]["Cloud Storage URL"].en.value;
    const viewerUrl = "https://legiongis.github.io/standalone-3dhop-viewer/";
    const iframeUrl = srcUrl ? `${viewerUrl}?model=${srcUrl}` : viewerUrl;

    document.getElementById('header-iframe').setAttribute('src', iframeUrl);
};

ko.components.register('three-d-hop', {
    viewModel: viewModel,
    template: template
});
