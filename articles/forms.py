from django import forms
from .models import Commentaire

class CommentCreateForm(forms.ModelForm):
    # username = forms.CharField(max_length=50, 
    #                            required=True, 
    #                            label="Entrez votre nom :")
    # contenu = forms.CharField(widget=forms.Textarea,
    #                           required=True)

    class Meta :
        model = Commentaire
        fields = ["name", "contenu"]
        widgets = {
            "contenu" : forms.Textarea(
                attrs={"rows":4, "placeholder": "Entrez votre commentaire ici.." }
                )
        }
    
    def clean_name(self):
        #Enlevez les espaces
        username = self.cleaned_data.get("name")
        if username != None :
            return username.strip().lower() 
        
    def clean_contenu(self):
        #Récupère la valeur du contenu du commentaire
        contenu_commentaire = self.cleaned_data["contenu"]

        #Verification
        if "bête" in contenu_commentaire :
            raise forms.ValidationError("Interdiction d'avoir des insultes dans les commentaires")
        
        return contenu_commentaire