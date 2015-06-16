"""Definition of the Provider content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from pcp.contenttypes.interfaces import IProvider
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ProviderSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ateapi.UrlField('url'),
    ateapi.AddressField('address'),
    BackReferenceField('affiliated',
                       relationship='affiliated',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('hosts',
                       relationship='hosted_by',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('projects_invloved',
                       relationship='provided_by',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Projects involved',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ProviderSchema,
    folderish=True,
    moveDiscussion=False
)


class Provider(folder.ATFolder, CommonUtilities):
    """Compute or data service provider"""
    implements(IProvider)

    meta_type = "Provider"
    schema = ProviderSchema


atapi.registerType(Provider, PROJECTNAME)