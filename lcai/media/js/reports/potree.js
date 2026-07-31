import ko from 'knockout';
import ReportViewModel from 'viewmodels/report';
import template from 'templates/views/report-templates/iframe-header.htm';

const viewModel = function(params) {
    params.configKeys = [];
    ReportViewModel.apply(this, [params]);

    const srcUrl = this.report?.report_json?.resource["3D Model Url"].en.value;
    const viewerUrl = "https://legiongis.github.io/standalone-potree-viewer/";
    const iframeUrl = srcUrl ? `${viewerUrl}?url=${srcUrl}` : viewerUrl;

    document.getElementById('header-iframe').setAttribute('src', iframeUrl);
};

ko.components.register('potree', {
    viewModel: viewModel,
    template: template
});
