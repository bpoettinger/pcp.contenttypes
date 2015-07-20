from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class ResolveID(BrowserView):
    """Resolve any id we may know about"""

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def resolve_id(self, id=None, verbose=False):
        """lookup the id passed in and redirect to content if 
        exactly one match is found.
        If no match is found it says so and a list of URLs
        i sretunr if the id resolves to more than one object."""

        if id is None:
            return None

        hits = self.catalog(ids=id)

        if not hits:
            if verbose:
                return "No object with id '%s' found" % id
            else:
                return None

        if len(hits) > 1:
            urls = [brain.getURL() for brain in hits]
            return urls

        url = hits[0].getURL()

        return self.request.response.redirect(url)
