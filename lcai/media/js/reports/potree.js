import ko from 'knockout';
import ReportViewModel from 'viewmodels/report';
import createVueApplication from 'utils/create-vue-application';
import PointCloudViewerIframe from '@/lcai/reports/PointCloudReportIframe.vue';
import template from 'templates/views/report-templates/potree.htm';

const viewModel = function(params) {
    params.configKeys = [];
    ReportViewModel.apply(this, [params]);

    const cloudJsUrl = this.report.report_json.resource["3D Model Url"].en.value;
    createVueApplication(PointCloudViewerIframe, undefined, {
            url: cloudJsUrl
        })
        .then(vueApp => vueApp.mount('#viewer-mount'))
        .catch(console.error);
};

ko.components.register('potree', {
    viewModel: viewModel,
    template: template
});
