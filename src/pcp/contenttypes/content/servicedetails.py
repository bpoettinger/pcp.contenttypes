"""Definition of the Service Details content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from Products.ATExtensions import ateapi

from pcp.contenttypes.interfaces import IServiceDetails
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ServiceDetailsSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.StringField('service_status',
                      widget=atapi.StringWidget(label='Status'),
                      ),
    atapi.StringField('version',
                      widget=atapi.StringWidget(label='Version'),
                      ),
    atapi.StringField('use_cases',
                      searchable=1,
                      widget=atapi.StringWidget(label='Use cases'),
                      ),
    atapi.StringField('features_current',
                      searchable=1,
                      widget=atapi.StringWidget(label='Current features'),
                      ),
    atapi.StringField('features_future',
                      searchable=1,
                      widget=atapi.StringWidget(label='Future features'),
                      ),
    atapi.ReferenceField('dependencies',
                         relationship='depends_on',
                         allowed_types=('Service',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Depends on',
                                                       allow_browse=1,
                                                       startup_directory='/catalog',
                                                       ),
                         ),
    ateapi.UrlField('usage_policy_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Usage policy'),
                    ),
    ateapi.UrlField('user_documentation_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='User documentation'),
                    ),
    ateapi.UrlField('operations_documentation_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Operations documentation'),
                    ),
    ateapi.UrlField('monitoring_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Monitoring'),
                    ),
    ateapi.UrlField('accounting_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Accounting'),
                    ),
    ateapi.UrlField('business_continuity_plan_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Business continuity plan'),
                    ),
    ateapi.UrlField('disaster_recovery_plan_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Disaster recovery plan'),
                    ),
    ateapi.UrlField('decommissioning_procedure_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Decommissioning procedure'),
                    ),
    atapi.StringField('cost_to_run',
                      searchable=1,
                      widget=atapi.StringWidget(label='Cost to build'),
                      ),
    atapi.StringField('cost_to_build',
                      searchable=1,
                      widget=atapi.StringWidget(label='Cost to build'),
                      ),
    atapi.StringField('service_details_type',
                      searchable=1,
                      widget=atapi.StringWidget(label='Details type'),
                      ),
    ateapi.RecordField('service_details',
                       subfields=('status', 'version', 'link', 'in_catalog'),
                       widget=ateapi.RecordWidget(label='Service details'),
                       ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ServiceDetailsSchema,
    folderish=True,
    moveDiscussion=False
)


class ServiceDetails(folder.ATFolder, CommonUtilities):
    """Detailed information about a service"""
    implements(IServiceDetails)

    meta_type = "ServiceDetails"
    schema = ServiceDetailsSchema


atapi.registerType(ServiceDetails, PROJECTNAME)
