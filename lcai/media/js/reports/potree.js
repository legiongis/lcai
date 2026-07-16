import ko from 'knockout';
import ReportViewModel from 'viewmodels/report';
import createVueApplication from 'utils/create-vue-application';
import PointCloudViewer from '@/lcai/reports/PointCloudReport.vue';
import template from 'templates/views/report-templates/potree.htm';

const viewModel = function(params) {
    params.configKeys = [];
    ReportViewModel.apply(this, [params]);

    const cloudJsUrl = this.report.report_json.resource["3D Model Url"].en.value;
    createVueApplication(PointCloudViewer, undefined, {
            url: cloudJsUrl
        })
        .then(vueApp => vueApp.mount('#my-plugin-mount'))
        .catch(console.error);
};

ko.components.register('potree', {
    viewModel: viewModel,
    template: template
});
