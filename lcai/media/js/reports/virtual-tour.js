import ko from 'knockout';
import ReportViewModel from 'viewmodels/report';
import template from 'templates/views/report-templates/iframe-header.htm';

const viewModel = function(params) {
    params.configKeys = [];
    ReportViewModel.apply(this, [params]);

    const iframeUrl = this.report?.report_json?.resource["Virtual Tours File Package"]["Cloud Storage URL"].url;
    document.getElementById('header-iframe').setAttribute('src', iframeUrl);
};

ko.components.register('virtual-tour', {
    viewModel: viewModel,
    template: template
});
