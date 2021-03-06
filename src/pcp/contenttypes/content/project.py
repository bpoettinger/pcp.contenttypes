"""Definition of the Project content type
"""

from pcp.contenttypes.interfaces import IRegisteredComputeResource
from pcp.contenttypes.interfaces import IRegisteredStorageResource
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IProject
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ProjectSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ateapi.UrlField('website'),
    atapi.ReferenceField('community',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='done_for',
                         allowed_types=('Community',),
                         widget=ReferenceBrowserWidget(label='Customer',
                                                       description='Main customer '
                                                       'involved in this project',
                                                       allow_browse=1,
                                                       startup_directory='/customers',
                                                       ),
                         ),
    atapi.ReferenceField('community_contact',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='community_contact',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Customer contact',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    # TODO: do we need this field at all?
    #    atapi.ReferenceField('services_used',
    #                         read_permission='View internals',
    #                         write_permission='Modify internals',
    #                         relationship='using',
    #                         multiValued=1,
    #                         allowed_types=('Service',),
    #                         widget=ReferenceBrowserWidget(label='Services used',
    #                                                       description="Select all services the project requires",
    #                                                       allow_browse=1,
    #                                                       startup_directory='/services',
    #                                                       condition='python:here.stateIn(["enabling","pre_production","production","terminated"])'),
    #
    atapi.ReferenceField('registered_services_used',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='using',
                         multiValued=1,
                         allowed_types=('RegisteredService',),
                         widget=ReferenceBrowserWidget(label='Registered services used',
                                                       description="Select all registered services the project requires",
                                                       allow_browse=1,
                                                       startup_directory='/operations',
                                                       condition='python:here.stateIn(["enabling","pre_production","production","terminated"])'),

                         ),
    #    ateapi.RecordField('resources',
    #                       subfields=('allocated (TB)', 'used (TB)', '# of objects'),
    #                       ),
    ateapi.RecordField('allocated',
                       subfields=('value', 'unit'),
                       subfield_vocabularies={'unit': 'informationUnits'},
                       widget=ateapi.RecordWidget(
                           condition='python:here.stateIn(["planned","enabling","pre_production","production","terminated"])'),
                       ),
    ateapi.RecordField('used',
                       subfields=('value', 'unit'),
                       subfield_vocabularies={'unit': 'informationUnits'},
                       widget=ateapi.RecordWidget(
                           condition='python:here.stateIn(["pre_production","production","terminated"])'),
                       ),
    atapi.ComputedField('allocated_new',
                        expression='here.sizeToString(here.convert(here.getSizeSummary()))',
                        widget=atapi.ComputedWidget(label='Allocated'),
                       ),
    atapi.ComputedField('used_new',
                        expression='here.sizeToString(here.convert(here.getUsedSummary()))',
                        widget=atapi.ComputedWidget(label='Used'),
                        ),
    atapi.ReferenceField('project_enabler',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='enabled_by',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Project enabled by',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       condition="python:here.stateNotIn(['considered'])",
                                                       ),
                         ),
    atapi.DateTimeField('start_date',
                        widget=atapi.CalendarWidget(label='Start date',
                                                    show_hm=False,
                                                    condition="python:here.stateNotIn(['considered'])",
                                                    ),
                        ),
    atapi.DateTimeField('end_date',
                        widget=atapi.CalendarWidget(label='End date',
                                                    show_hm=False,
                                                    condition="python:here.stateNotIn(['considered'])",
                                                    ),
                        ),
    ateapi.UrlField('call_for_collaboration',
                    widget=ateapi.UrlWidget(label='Call for collaboration',
                                            description='URL to the call that '
                                            'triggered this project',
                                            ),
                    ),
    ateapi.UrlField('uptake_plan',
                    read_permission='View internals',
                    write_permission='Modify internals',
                    widget=ateapi.UrlWidget(label='Uptake plan',
                                            description='URL to the project '
                                            'uptake plan (if not available on this site). '
                                            'Otherwise, often found on the '
                                            'confluence site.',
                                            ),
                    ),
    atapi.StringField('repository',
                      widget=atapi.StringWidget(description="If the data to be "
                                                "dealt with here are in a web-accessible "
                                                "repository already you should specify "
                                                "its URL here.",),
                      ),
    atapi.StringField('topics',
                      widget=atapi.StringWidget(description='Please mention the '
                                                'scientific field(s) the data '
                                                'originate from.'),
                      ),
    BackReferenceField('resources',
                       relationship='project',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Resources',
                                                  visible={
                                                      'edit': 'invisible'},
                                                  ),
                       ),
    atapi.ComputedField('resource_usage',
                  expression='here.getResourceUsage()',
                  widget=atapi.ComputedWidget(label='Resource Usage'),
                  ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ProjectSchema,
    folderish=True,
    moveDiscussion=False
)


class Project(folder.ATFolder, CommonUtilities):
    """A project managed by this site."""
    implements(IProject)

    meta_type = "Project"
    schema = ProjectSchema

    def getAllocated(self):
        """Specialized accessor that can handle unit conversions."""
        raw = self.schema['allocated'].get(self)
        return self.convert(raw)

    def getUsed(self):
        """Specialized accessor supporting unit conversion"""
        raw = self.schema['used'].get(self)
        return self.convert(raw)

    def getResourceUsage(self):
        usages = []
        for resource in self.getResources():
            if IRegisteredStorageResource.providedBy(resource):
                used = resource.getUsedMemory()
                size = resource.getAllocatedMemory()

                if size:
                    size = self.convert(size)
                    size_value = float(size['value'])
                    size_unit = size['unit']
                    size_str = '%0.2f %s' % (size_value, size_unit)
                else:
                    size_str = '??'
                    size_value = None

                if used:
                    core = self.convert_pure(used['core'])
                    core_value = float(core['value'])
                    used_str = '%0.2f %s' % (core_value, core['unit'])
                    meta = used['meta']
                    submission_time = meta['submission_time']
                    core_in_size_unit = self.convert_pure(used['core'], size_unit)
                    core_value_in_size_unit = float(core_in_size_unit['value'])
                else:
                    core_value = None
                    used_str = '??'
                    submission_time = '??'

                if core_value and size_value:
                    rel_usage_str = '%0.2f' % (core_value_in_size_unit / size_value * 100.0)
                else:
                    rel_usage_str = '??'

                usages.append('%s: %s / %s (%s%%) (%s UTC)' %
                              (resource.title, used_str, size_str, rel_usage_str, submission_time))

            if IRegisteredComputeResource.providedBy(resource):
                pass

        return '<br>'.join(usages)

    def getUsedSummary(self):
        value = 0
        unit = 'B'

        for resource in self.getResources():
            if IRegisteredStorageResource.providedBy(resource):
                used = resource.getUsedMemory()
                if used:
                    used_bytes = self.convert_pure(used['core'], unit)
                    value += float(used_bytes['value'])
                else:
                    return None

        return {'value': value, 'unit': unit}

    def getSizeSummary(self):
        value = 0
        unit = 'B'

        for resource in self.getResources():
            if IRegisteredStorageResource.providedBy(resource):
                size = resource.getAllocatedMemory()
                if size:
                    size_bytes = self.convert_pure(size, unit)
                    value += float(size_bytes['value'])
                else:
                    return None

        return {'value': value, 'unit': unit}



atapi.registerType(Project, PROJECTNAME)
