"""Definition of the Resource content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IResource
from pcp.contenttypes.config import PROJECTNAME

ResourceSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.ReferenceField('managed_by',
                         relationship='managed_by',
                         allowed_types=('Person',),
                         widget=atapi.ReferenceWidget(label='Managed by',
                                                      ),
                         ),
    atapi.ReferenceField('hosted_by',
                         relationship='hosted_by',
                         allowed_types=('Center',),
                         widget=atapi.ReferenceWidget(label='Hosted by',
                                                      ),
                        ),
    atapi.ReferenceField('used_by',
                         relationship='used_by',
                         allowed_types=('Service',),
                         widget=atapi.ReferenceWidget(label='Used by',
                                                      ),
                        ),                     
))


schemata.finalizeATCTSchema(
    ResourceSchema,
    folderish=True,
    moveDiscussion=False
)


class Resource(folder.ATFolder):
    """A resource needed to provide a service managed by a project on this site."""
    implements(IResource)

    meta_type = "Resource"
    schema = ResourceSchema


atapi.registerType(Resource, PROJECTNAME)
