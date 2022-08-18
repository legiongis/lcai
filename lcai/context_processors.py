from arches.app.models.models import ResourceInstance

def load_3d_libraries(request):
    load_potree_libs, load_3dhop_libs = False, False
    path = request.get_full_path().lstrip("/")
    if "report" in path:
        comps = path.split("/")
        if len(comps) > 1:
            resid = comps[-1]
            try:
                res = ResourceInstance.objects.get(pk=resid)
                # hard-coded id for resource model that uses potree viewer
                if str(res.graph_id) == "9b591814-c0f2-11e8-9c8c-0242ac120004":
                    load_potree_libs = True
                # hard-coded id for resource model that uses 3DHOP viewer
                if str(res.graph_id) == "36bcaff4-b82f-11e8-8598-0242ac120004":
                    load_3dhop_libs = True
            except Exception as e:
                pass
    # short-circuiting this for now and loading everything all the time.
    # it seems like even for the 3dhop report, the potree.js component is loaded,
    # meaning that all of its dependencies must also be loaded. this shouldn't
    # be the case but apparently is for now.
    load_potree_libs, load_3dhop_libs = True, True
    return {
        "load_potree_libs": load_potree_libs,
        "load_3dhop_libs": load_3dhop_libs
    }