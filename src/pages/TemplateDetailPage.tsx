import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Header } from "../components/Header";
import { Footer } from "../components/Footer";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { ImageWithFallback } from "../components/figma/ImageWithFallback";
import { ArrowLeft, Download, Eye, Edit2, Check, Loader } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useAPI } from "../hooks/useAPI";
import { toast } from "sonner";

// Templates data - à synchroniser avec TemplatesPage
const allTemplates = [
  {
    id: 1,
    title: "Fashion Store",
    category: "Mode",
    image: "https://images.unsplash.com/photo-1761090617068-f1b3257d27ad?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmYXNoaW9uJTIwYm91dGlxdWUlMjBzdG9yZXxlbnwxfHx8fDE3NjQ1NjY4NjR8MA&ixlib=rb-4.1.0&q=80&w=1080",
    description: "Template élégant pour boutique de mode avec galerie produits",
    features: ["Galerie de mode", "Panier achats", "Paiement sécurisé"],
    colors: {
      primary: "#0077FF",
      secondary: "#5AC8FA",
      accent: "#FF6B6B",
    },
    components: {
      storeName: "Fashion Store",
      tagline: "Découvrez les dernières tendances",
      heroText: "Bienvenue dans notre boutique de mode exclusive",
    },
  },
  {
    id: 2,
    title: "Urban Style",
    category: "Mode",
    image: "https://images.unsplash.com/photo-1745716154e27b97f8c73b39a9ef3de5a09efd08?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Style urbain et contemporain pour vêtements tendance",
    features: ["Design moderne", "Filtres produits", "Avis clients"],
    colors: {
      primary: "#0A1A2F",
      secondary: "#5AC8FA",
      accent: "#FF6B6B",
    },
    components: {
      storeName: "Urban Style",
      tagline: "Mode urbaine et contemporaine",
      heroText: "Exprimez votre style unique",
    },
  },
  {
    id: 3,
    title: "Luxury Couture",
    category: "Mode",
    image: "https://images.unsplash.com/photo-1770566174775-f37a92f3370f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Template premium pour haute couture et luxe",
    features: ["Design raffiné", "Showroom virtuel", "Collections VIP"],
    colors: {
      primary: "#1A1A1A",
      secondary: "#D4AF37",
      accent: "#C0C0C0",
    },
    components: {
      storeName: "Luxury Couture",
      tagline: "Haute couture et élégance",
      heroText: "Bienvenue dans le monde du luxe",
    },
  },
  {
    id: 4,
    title: "Tech Shop",
    category: "High-tech",
    image: "https://images.unsplash.com/photo-1761207850745-d41a776ef897?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwZ2FkZ2V0cyUyMHNob3B8ZW58MXx8fHwxNzY0NjEyMDY4fDA&ixlib=rb-4.1.0&q=80&w=1080",
    description: "Design moderne pour produits technologiques",
    features: ["Spécifications détaillées", "Comparaison produits", "Support technique"],
    colors: {
      primary: "#0077FF",
      secondary: "#00D9FF",
      accent: "#FF6B6B",
    },
    components: {
      storeName: "Tech Shop",
      tagline: "Innovation technologique",
      heroText: "Les meilleurs gadgets et appareils",
    },
  },
  {
    id: 5,
    title: "Gadget Pro",
    category: "High-tech",
    image: "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Pour les dernières innovations et gadgets",
    features: ["Critiques produits", "Notifications de stock", "Programme fidélité"],
    colors: {
      primary: "#0077FF",
      secondary: "#5AC8FA",
      accent: "#FF6B6B",
    },
    components: {
      storeName: "Gadget Pro",
      tagline: "Les gadgets du futur",
      heroText: "Découvrez les innovations avant tout le monde",
    },
  },
  {
    id: 6,
    title: "Electronics Hub",
    category: "High-tech",
    image: "https://images.unsplash.com/photo-1505228395891-9a51e7e86e81?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Centre complet pour appareils électroniques",
    features: ["Blog technologie", "Conseils d'experts", "Garantie étendue"],
    colors: {
      primary: "#0077FF",
      secondary: "#5AC8FA",
      accent: "#FF6B6B",
    },
    components: {
      storeName: "Electronics Hub",
      tagline: "Électronique et technologie",
      heroText: "Tous vos appareils électroniques en un lieu",
    },
  },
  {
    id: 7,
    title: "Beauty Haven",
    category: "Beauté",
    image: "https://images.unsplash.com/photo-1624574966266-1cdd65b74500?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxiZWF1dHklMjBjb3NtZXRpY3MlMjBwcm9kdWN0c3xlbnwxfHx8fDE3NjQ1NzI3OTd8MA&ixlib=rb-4.1.0&q=80&w=1080",
    description: "Template raffiné pour cosmétiques et soins",
    features: ["Guides beauté", "Consultations", "Programmes fidélité"],
    colors: {
      primary: "#FF6B9D",
      secondary: "#FFC0CB",
      accent: "#FF1493",
    },
    components: {
      storeName: "Beauty Haven",
      tagline: "Beauté et cosmétiques premium",
      heroText: "Découvrez votre beauté naturelle",
    },
  },
  {
    id: 8,
    title: "Glow Beauty",
    category: "Beauté",
    image: "https://images.unsplash.com/photo-1576426394840-c51e7f1dc5d8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Soins et beauté haut de gamme",
    features: ["Recommandations IA", "Test produits", "Tutoriels vidéo"],
    colors: {
      primary: "#FF6B9D",
      secondary: "#FFC0CB",
      accent: "#FF1493",
    },
    components: {
      storeName: "Glow Beauty",
      tagline: "Brillez naturellement",
      heroText: "Soins et beauté pour votre meilleure version",
    },
  },
];

export function TemplateDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const api = useAPI();
  const template = allTemplates.find(t => t.id === parseInt(id || "0"));

  const [isEditMode, setIsEditMode] = useState(false);
  const defaultSettings = {
    fontFamily: "Inter",
    layout: "grid",
    showHeader: true,
    buttonStyle: "rounded",
    heroImage: template?.image || allTemplates[0].image,
    logoUrl: "",
    fontSize: "16",
    showFooter: true,
    productColumns: 3,
    productCardStyle: "shadow",
    showSearch: true,
    currency: "EUR",
    socialLinks: { facebook: "", instagram: "", whatsapp: "" },
  };

  const [editedTemplate, setEditedTemplate] = useState(
    template ? { ...template, settings: template.settings || defaultSettings } : { ...allTemplates[0], settings: defaultSettings }
  );
  const [showPreview, setShowPreview] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [isCreating, setIsCreating] = useState(false);

  if (!template) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-950">
        <Header />
        <div className="container mx-auto px-6 py-24 text-center">
          <h1 className="text-3xl font-bold text-[#0A1A2F] mb-4">Template non trouvé</h1>
          <Button
            onClick={() => navigate("/templates")}
            className="bg-[#0077FF] hover:bg-[#0077FF]/90 text-white rounded-xl px-8 h-12"
          >
            Retour aux templates
          </Button>
        </div>
        <Footer />
      </div>
    );
  }

  const handleEdit = (field: string, value: string) => {
    setEditedTemplate({
      ...editedTemplate,
      components: {
        ...editedTemplate.components,
        [field]: value,
      },
    });
  };

  const handleColorChange = (colorKey: string, value: string) => {
    setEditedTemplate({
      ...editedTemplate,
      colors: {
        ...editedTemplate.colors,
        [colorKey]: value,
      },
    });
  };

  const handleSettingChange = (key: string, value: any) => {
    setEditedTemplate({
      ...editedTemplate,
      settings: {
        ...editedTemplate.settings,
        [key]: value,
      },
    });
  };

  const handleSaveAndUse = async () => {
    setIsCreating(true);
    try {
      // Vérifier que l'utilisateur est connecté
      if (!user) {
        toast.error("Vous devez être connecté pour créer une boutique");
        navigate("/login");
        return;
      }

      // Préparer les données de la boutique
      const shopData = {
        name: editedTemplate.components.storeName,
        description: editedTemplate.components.heroText,
        email: user.email,
        phone: user.phone_number || "",
        template_id: editedTemplate.id,
        template_config: {
          colors: editedTemplate.colors,
          components: editedTemplate.components,
          title: editedTemplate.title,
          category: editedTemplate.category,
        },
      };

      console.log("🏪 Création de la boutique avec template:", shopData);

      // Créer la boutique via l'API
      const res = await api.post("/shop/api/create/", shopData);

      if (!res.ok) {
        const error = await res.json().catch(() => ({}));
        const msg = error?.detail || "Erreur lors de la création de la boutique";
        toast.error(msg);
        setIsCreating(false);
        return;
      }

      const shopResponse = await res.json();
      console.log("✅ Boutique créée:", shopResponse);

      // Sauvegarder les données du template et de la boutique
      localStorage.setItem("selectedTemplate", JSON.stringify(editedTemplate));
      localStorage.setItem("createdShop", JSON.stringify(shopResponse));

      toast.success("Boutique créée avec succès! Redirection...");
      setSaveSuccess(true);

      // Rediriger vers My Shop après un court délai
      setTimeout(() => {
        navigate("/my-shop", { state: { shopCreated: true } });
      }, 1500);
    } catch (error: any) {
      console.error("❌ Erreur lors de la création:", error);
      toast.error(error?.message || "Erreur lors de la création de la boutique");
      setIsCreating(false);
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-gray-950">
      <Header />

      <section className="py-12 bg-gradient-to-br from-[#0077FF]/5 to-white">
        <div className="container mx-auto px-6">
          {/* Breadcrumb & Back */}
          <button
            onClick={() => navigate("/templates")}
            className="flex items-center gap-2 text-[#0077FF] hover:text-[#0077FF]/80 mb-8 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Retour aux templates
          </button>

          <div className="grid lg:grid-cols-2 gap-12">
            {/* Aperçu du Template */}
            <div className="space-y-6">
              <div className="rounded-2xl overflow-hidden border-2 border-gray-200 shadow-lg">
                <ImageWithFallback
                  src={editedTemplate.image}
                  alt={editedTemplate.title}
                  className="w-full h-96 object-cover"
                />
              </div>

              <div className="space-y-4">
                <h1 className="text-4xl font-bold text-[#0A1A2F]">{editedTemplate.title}</h1>
                <p className="text-xl text-[#0A1A2F]/70">{editedTemplate.description}</p>

                <div className="flex flex-wrap gap-2">
                  {editedTemplate.features.map((feature, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-[#0077FF]/10 text-[#0077FF] rounded-full text-sm font-medium"
                    >
                      {feature}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-6 border-t border-gray-200 space-y-3">
                <Button
                  onClick={handleSaveAndUse}
                  className="w-full bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] text-white hover:shadow-lg rounded-xl h-14 font-semibold transition-all flex items-center justify-center gap-2"
                  disabled={saveSuccess || isCreating}
                >
                  {isCreating && <Loader className="w-5 h-5 animate-spin" />}
                  {saveSuccess ? "✓ Boutique créée" : isCreating ? "Création en cours..." : "Utiliser ce template"}
                </Button>
                <Button
                  onClick={() => setIsEditMode(!isEditMode)}
                  variant="outline"
                  className="w-full border-2 border-[#0077FF] text-[#0077FF] hover:bg-[#0077FF]/5 rounded-xl h-14 font-semibold transition-all"
                  disabled={isCreating}
                >
                  <Edit2 className="w-5 h-5 mr-2" />
                  {isEditMode ? "Voir l'aperçu" : "Modifier"}
                </Button>
              </div>
            </div>

            {/* Panneau d'édition */}
            {isEditMode && (
              <div className="space-y-8 bg-gray-50 p-8 rounded-2xl border-2 border-gray-200">
                <div>
                  <h2 className="text-2xl font-bold text-[#0A1A2F] mb-6">Personnalisez votre template</h2>

                  {/* Informations du magasin */}
                  <div className="space-y-4 mb-8 pb-8 border-b border-gray-300">
                    <h3 className="text-lg font-semibold text-[#0A1A2F]">Informations du magasin</h3>

                    <div>
                      <label className="block text-sm font-medium text-[#0A1A2F] mb-2">
                        Nom du magasin
                      </label>
                      <Input
                        value={editedTemplate.components.storeName}
                        onChange={(e) => handleEdit("storeName", e.target.value)}
                        className="w-full h-12 rounded-xl border-2 border-gray-300 focus:border-[#0077FF]"
                        placeholder="Entrez le nom de votre magasin"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-[#0A1A2F] mb-2">
                        Slogan / Tagline
                      </label>
                      <Input
                        value={editedTemplate.components.tagline}
                        onChange={(e) => handleEdit("tagline", e.target.value)}
                        className="w-full h-12 rounded-xl border-2 border-gray-300 focus:border-[#0077FF]"
                        placeholder="Votre slogan"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-[#0A1A2F] mb-2">
                        Texte d'accueil
                      </label>
                      <textarea
                        value={editedTemplate.components.heroText}
                        onChange={(e) => handleEdit("heroText", e.target.value)}
                        className="w-full p-3 rounded-xl border-2 border-gray-300 focus:border-[#0077FF] min-h-24 font-sans"
                        placeholder="Texte d'accueil principal"
                      />
                    </div>
                  </div>

                  {/* Personnalisation des couleurs */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-[#0A1A2F]">Couleurs de votre marque</h3>

                    <div>
                      <label className="block text-sm font-medium text-[#0A1A2F] mb-2">
                        Couleur primaire
                      </label>
                      <div className="flex gap-3">
                        <input
                          type="color"
                          value={editedTemplate.colors.primary}
                          onChange={(e) => handleColorChange("primary", e.target.value)}
                          className="w-16 h-12 rounded-lg cursor-pointer border-2 border-gray-300"
                        />
                        <Input
                          value={editedTemplate.colors.primary}
                          onChange={(e) => handleColorChange("primary", e.target.value)}
                          className="flex-1 h-12 rounded-xl border-2 border-gray-300 focus:border-[#0077FF]"
                          placeholder="#000000"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-[#0A1A2F] mb-2">
                        Couleur secondaire
                      </label>
                      <div className="flex gap-3">
                        <input
                          type="color"
                          value={editedTemplate.colors.secondary}
                          onChange={(e) => handleColorChange("secondary", e.target.value)}
                          className="w-16 h-12 rounded-lg cursor-pointer border-2 border-gray-300"
                        />
                        <Input
                          value={editedTemplate.colors.secondary}
                          onChange={(e) => handleColorChange("secondary", e.target.value)}
                          className="flex-1 h-12 rounded-xl border-2 border-gray-300 focus:border-[#0077FF]"
                          placeholder="#000000"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-[#0A1A2F] mb-2">
                        Couleur accent
                      </label>
                      <div className="flex gap-3">
                        <input
                          type="color"
                          value={editedTemplate.colors.accent}
                          onChange={(e) => handleColorChange("accent", e.target.value)}
                          className="w-16 h-12 rounded-lg cursor-pointer border-2 border-gray-300"
                        />
                        <Input
                          value={editedTemplate.colors.accent}
                          onChange={(e) => handleColorChange("accent", e.target.value)}
                          className="flex-1 h-12 rounded-xl border-2 border-gray-300 focus:border-[#0077FF]"
                          placeholder="#000000"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Nouveaux contrôles: police, layout, hero image, header, style bouton */}
                  <div className="pt-6 border-t border-gray-200 space-y-4">
                    <h3 className="text-lg font-semibold text-[#0A1A2F]">Plus d'options</h3>

                    <div>
                      <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Police</label>
                      <select
                        value={editedTemplate.settings.fontFamily}
                        onChange={(e) => handleSettingChange("fontFamily", e.target.value)}
                        className="w-full h-12 rounded-xl border-2 border-gray-300"
                      >
                        <option value="Inter">Inter (sans-serif)</option>
                        <option value="Roboto">Roboto (sans-serif)</option>
                        <option value="Poppins">Poppins (sans-serif)</option>
                        <option value="Georgia">Georgia (serif)</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Layout produits</label>
                      <select
                        value={editedTemplate.settings.layout}
                        onChange={(e) => handleSettingChange("layout", e.target.value)}
                        className="w-full h-12 rounded-xl border-2 border-gray-300"
                      >
                        <option value="grid">Grille</option>
                        <option value="list">Liste</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Image Hero (URL)</label>
                      <Input
                        value={editedTemplate.settings.heroImage}
                        onChange={(e) => handleSettingChange("heroImage", e.target.value)}
                        className="w-full h-12 rounded-xl border-2 border-gray-300"
                        placeholder="https://..."
                      />
                    </div>

                    <div className="flex gap-4">
                      <div className="flex-1">
                        <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Afficher le header</label>
                        <select
                          value={editedTemplate.settings.showHeader ? "yes" : "no"}
                          onChange={(e) => handleSettingChange("showHeader", e.target.value === "yes")}
                          className="w-full h-12 rounded-xl border-2 border-gray-300"
                        >
                          <option value="yes">Oui</option>
                          <option value="no">Non</option>
                        </select>
                      </div>

                      <div className="flex-1">
                        <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Style des boutons</label>
                        <select
                          value={editedTemplate.settings.buttonStyle}
                          onChange={(e) => handleSettingChange("buttonStyle", e.target.value)}
                          className="w-full h-12 rounded-xl border-2 border-gray-300"
                        >
                          <option value="rounded">Arrondi</option>
                          <option value="pill">Pill</option>
                          <option value="square">Carré</option>
                        </select>
                      </div>
                    </div>

                    <div className="pt-4">
                      <Button
                        onClick={() => {
                          localStorage.setItem("selectedTemplate", JSON.stringify(editedTemplate));
                          toast.success("Configuration enregistrée localement");
                        }}
                        className="w-full bg-[#0A1A2F] text-white rounded-xl h-12"
                      >
                        Enregistrer la configuration
                      </Button>
                    </div>

                    {/* Autres options */}
                    <div className="pt-6 border-t border-gray-200 space-y-4">
                      <h3 className="text-lg font-semibold text-[#0A1A2F]">Autres options</h3>

                      <div>
                        <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Logo (URL)</label>
                        <Input
                          value={editedTemplate.settings.logoUrl}
                          onChange={(e) => handleSettingChange("logoUrl", e.target.value)}
                          className="w-full h-12 rounded-xl border-2 border-gray-300"
                          placeholder="https://.../logo.png"
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Taille de police (px)</label>
                          <Input
                            value={editedTemplate.settings.fontSize}
                            onChange={(e) => handleSettingChange("fontSize", e.target.value)}
                            className="w-full h-12 rounded-xl border-2 border-gray-300"
                            placeholder="16"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Afficher le footer</label>
                          <select
                            value={editedTemplate.settings.showFooter ? "yes" : "no"}
                            onChange={(e) => handleSettingChange("showFooter", e.target.value === "yes")}
                            className="w-full h-12 rounded-xl border-2 border-gray-300"
                          >
                            <option value="yes">Oui</option>
                            <option value="no">Non</option>
                          </select>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Colonnes produits</label>
                          <select
                            value={editedTemplate.settings.productColumns}
                            onChange={(e) => handleSettingChange("productColumns", parseInt(e.target.value))}
                            className="w-full h-12 rounded-xl border-2 border-gray-300"
                          >
                            <option value={1}>1</option>
                            <option value={2}>2</option>
                            <option value={3}>3</option>
                            <option value={4}>4</option>
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Style carte produit</label>
                          <select
                            value={editedTemplate.settings.productCardStyle}
                            onChange={(e) => handleSettingChange("productCardStyle", e.target.value)}
                            className="w-full h-12 rounded-xl border-2 border-gray-300"
                          >
                            <option value="shadow">Ombre</option>
                            <option value="flat">Plat</option>
                          </select>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Afficher la recherche</label>
                          <select
                            value={editedTemplate.settings.showSearch ? "yes" : "no"}
                            onChange={(e) => handleSettingChange("showSearch", e.target.value === "yes")}
                            className="w-full h-12 rounded-xl border-2 border-gray-300"
                          >
                            <option value="yes">Oui</option>
                            <option value="no">Non</option>
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Devise</label>
                          <Input
                            value={editedTemplate.settings.currency}
                            onChange={(e) => handleSettingChange("currency", e.target.value)}
                            className="w-full h-12 rounded-xl border-2 border-gray-300"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-[#0A1A2F] mb-2">Réseaux sociaux (URLs)</label>
                        <div className="grid grid-cols-3 gap-3">
                          <Input
                            value={editedTemplate.settings.socialLinks.facebook}
                            onChange={(e) => handleSettingChange("socialLinks", { ...editedTemplate.settings.socialLinks, facebook: e.target.value })}
                            placeholder="Facebook"
                            className="h-12 rounded-xl border-2 border-gray-300"
                          />
                          <Input
                            value={editedTemplate.settings.socialLinks.instagram}
                            onChange={(e) => handleSettingChange("socialLinks", { ...editedTemplate.settings.socialLinks, instagram: e.target.value })}
                            placeholder="Instagram"
                            className="h-12 rounded-xl border-2 border-gray-300"
                          />
                          <Input
                            value={editedTemplate.settings.socialLinks.whatsapp}
                            onChange={(e) => handleSettingChange("socialLinks", { ...editedTemplate.settings.socialLinks, whatsapp: e.target.value })}
                            placeholder="WhatsApp"
                            className="h-12 rounded-xl border-2 border-gray-300"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Aperçu en direct */}
            {!isEditMode && (
              <div className="space-y-6 bg-gradient-to-br from-[#0077FF]/5 to-[#5AC8FA]/5 p-8 rounded-2xl border-2 border-[#0077FF]/20">
                <h2 className="text-2xl font-bold text-[#0A1A2F]">Aperçu en direct</h2>

                <div
                  className="space-y-4 bg-white rounded-xl p-8 shadow-md border-2 border-gray-100"
                  style={{
                    fontFamily: (() => {
                      const map: any = {
                        Inter: "Inter, system-ui, sans-serif",
                        Roboto: "Roboto, system-ui, sans-serif",
                        Poppins: "Poppins, system-ui, sans-serif",
                        Georgia: "Georgia, serif",
                      };
                      return map[editedTemplate.settings?.fontFamily] || editedTemplate.settings?.fontFamily;
                    })(),
                    fontSize: editedTemplate.settings?.fontSize + "px",
                  }}
                >
                  {/* Header preview */}
                  {editedTemplate.settings?.showHeader && (
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-4">
                        {editedTemplate.settings?.logoUrl ? (
                          <img src={editedTemplate.settings.logoUrl} alt="logo" className="h-10 w-auto" />
                        ) : (
                          <div className="text-xl font-bold" style={{ color: editedTemplate.colors.primary }}>{editedTemplate.components.storeName}</div>
                        )}
                      </div>
                      {editedTemplate.settings?.showSearch && (
                        <div className="w-1/3">
                          <input className="w-full h-10 rounded-xl border-2 border-gray-200 p-2" placeholder="Rechercher des produits..." />
                        </div>
                      )}
                    </div>
                  )}
                  {/* Aperçu des couleurs */}
                  <div className="space-y-3">
                    <h3 className="font-semibold text-[#0A1A2F]">Palette de couleurs</h3>
                    <div className="grid grid-cols-3 gap-3">
                      <div className="space-y-2">
                        <div
                          className="w-full h-16 rounded-lg border-2 border-gray-200"
                          style={{ backgroundColor: editedTemplate.colors.primary }}
                        />
                        <p className="text-xs text-center text-gray-600">Primaire</p>
                      </div>
                      <div className="space-y-2">
                        <div
                          className="w-full h-16 rounded-lg border-2 border-gray-200"
                          style={{ backgroundColor: editedTemplate.colors.secondary }}
                        />
                        <p className="text-xs text-center text-gray-600">Secondaire</p>
                      </div>
                      <div className="space-y-2">
                        <div
                          className="w-full h-16 rounded-lg border-2 border-gray-200"
                          style={{ backgroundColor: editedTemplate.colors.accent }}
                        />
                        <p className="text-xs text-center text-gray-600">Accent</p>
                      </div>
                    </div>
                  </div>

                  {/* Aperçu du texte et hero */}
                  <div className="space-y-4 pt-6 border-t border-gray-200">
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Nom du magasin</p>
                      <h3 className="text-2xl font-bold" style={{ color: editedTemplate.colors.primary }}>
                        {editedTemplate.components.storeName}
                      </h3>
                    </div>

                    <div>
                      <p className="text-xs text-gray-600 mb-1">Slogan</p>
                      <p className="text-lg" style={{ color: editedTemplate.colors.secondary }}>
                        {editedTemplate.components.tagline}
                      </p>
                    </div>

                    <div>
                      <p className="text-xs text-gray-600 mb-1">Image & Texte d'accueil</p>
                      <div className="rounded-xl overflow-hidden border-2 border-gray-200">
                        <ImageWithFallback
                          src={editedTemplate.settings?.heroImage || editedTemplate.image}
                          alt="Hero"
                          className="w-full h-48 object-cover"
                        />
                      </div>
                      <p className="text-[#0A1A2F] leading-relaxed mt-3">{editedTemplate.components.heroText}</p>
                    </div>
                  </div>

                  {/* Boutons d'action (style selon option) */}
                  <div className="pt-6 border-t border-gray-200 space-y-2">
                    <button
                      className={`w-full py-3 font-semibold text-white transition-all ${
                        editedTemplate.settings?.buttonStyle === "pill" ? "rounded-full" : editedTemplate.settings?.buttonStyle === "square" ? "rounded-none" : "rounded-lg"
                      }`}
                      style={{ background: `linear-gradient(90deg, ${editedTemplate.colors.primary}, ${editedTemplate.colors.secondary})` }}
                    >
                      Découvrir nos produits
                    </button>
                    <button
                      className={`w-full py-3 font-semibold transition-all ${
                        editedTemplate.settings?.buttonStyle === "pill" ? "rounded-full" : editedTemplate.settings?.buttonStyle === "square" ? "rounded-none" : "rounded-lg"
                      }`}
                      style={{ borderColor: editedTemplate.colors.secondary, color: editedTemplate.colors.secondary }}
                    >
                      En savoir plus
                    </button>
                  </div>

                  {/* Mock product grid preview */}
                  <div className="pt-8">
                    <h4 className="text-lg font-semibold mb-4">Aperçu produits</h4>
                    <div className={`grid gap-4 ${editedTemplate.settings?.productColumns === 1 ? 'grid-cols-1' : editedTemplate.settings?.productColumns === 2 ? 'grid-cols-2' : editedTemplate.settings?.productColumns === 4 ? 'grid-cols-4' : 'grid-cols-3'}`}>
                      {[1,2,3,4,5,6].map((i) => (
                        <div key={i} className={`p-4 bg-white border rounded-lg ${editedTemplate.settings?.productCardStyle === 'shadow' ? 'shadow-md' : ''}`}>
                          <div className="h-32 bg-gray-100 mb-3 rounded-md" />
                          <div className="font-semibold">Produit exemple {i}</div>
                          <div className="text-sm text-gray-600">{editedTemplate.settings?.currency} { (19.99 + i).toFixed(2) }</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Footer preview */}
                  {editedTemplate.settings?.showFooter && (
                    <div className="mt-8 pt-6 border-t border-gray-200">
                      <div className="flex items-center justify-between">
                        <div className="text-sm">© {new Date().getFullYear()} {editedTemplate.components.storeName}</div>
                        <div className="flex items-center gap-3 text-sm">
                          {editedTemplate.settings?.socialLinks.facebook && <a href={editedTemplate.settings.socialLinks.facebook}>📘</a>}
                          {editedTemplate.settings?.socialLinks.instagram && <a href={editedTemplate.settings.socialLinks.instagram}>📸</a>}
                          {editedTemplate.settings?.socialLinks.whatsapp && <a href={editedTemplate.settings.socialLinks.whatsapp}>💬</a>}
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                <div className="pt-4 text-center text-sm text-gray-600">Cliquez sur "Modifier" pour personnaliser cet aperçu</div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Étapes de création */}
      <section className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-4xl font-bold text-[#0A1A2F] mb-4">
              Comment utiliser ce template
            </h2>
            <p className="text-xl text-[#0A1A2F]/70">
              En 4 étapes simples, transformez ce template en votre boutique en ligne
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                step: 1,
                title: "Personnaliser",
                description: "Modifiez les couleurs, textes et images selon votre marque",
                icon: "✏️",
              },
              {
                step: 2,
                title: "Ajouter des produits",
                description: "Importez votre catalogue complet de produits",
                icon: "📦",
              },
              {
                step: 3,
                title: "Configurer les paiements",
                description: "Connectez votre moyen de paiement (Stripe, PayPal, etc)",
                icon: "💳",
              },
              {
                step: 4,
                title: "Publier",
                description: "Lancez votre boutique et commencez à vendre",
                icon: "🚀",
              },
            ].map((item) => (
              <div key={item.step} className="relative">
                <div className="flex flex-col items-center text-center">
                  <div
                    className="w-16 h-16 rounded-full flex items-center justify-center mb-4 text-2xl"
                    style={{ backgroundColor: `${template.colors.primary}20` }}
                  >
                    {item.icon}
                  </div>
                  <div
                    className="inline-flex items-center justify-center w-8 h-8 rounded-full text-white text-sm font-bold mb-4"
                    style={{ backgroundColor: template.colors.primary }}
                  >
                    {item.step}
                  </div>
                  <h3 className="text-lg font-semibold text-[#0A1A2F] mb-2">{item.title}</h3>
                  <p className="text-[#0A1A2F]/70 text-sm">{item.description}</p>
                </div>

                {/* Connecteur vers la prochaine étape */}
                {item.step < 4 && (
                  <div
                    className="hidden lg:block absolute top-8 right-0 w-8 h-1 translate-x-1/2"
                    style={{ backgroundColor: `${template.colors.primary}40` }}
                  />
                )}
              </div>
            ))}
          </div>

          {/* Section Fonctionnalités incluses */}
          <div className="mt-20 bg-gradient-to-br from-[#0077FF]/5 to-[#5AC8FA]/5 rounded-2xl p-12 border border-[#0077FF]/20">
            <h3 className="text-2xl font-bold text-[#0A1A2F] mb-8 text-center">
              Fonctionnalités incluses dans ce template
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              {[
                { title: "Responsive Design", desc: "Fonctionne parfaitement sur tous les appareils" },
                { title: "SEO Optimisé", desc: "Meilleur classement dans les moteurs de recherche" },
                { title: "Panier intelligent", desc: "Gestion automatique du panier et des commandes" },
                { title: "Sécurité garantie", desc: "Certificat SSL et protection des données" },
                { title: "Analytics intégrées", desc: "Suivi complet de vos ventes et visiteurs" },
                { title: "Support client 24/7", desc: "Equipe dédiée pour vous aider" },
              ].map((feature, idx) => (
                <div key={idx} className="flex gap-4">
                  <div
                    className="w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 mt-1"
                    style={{ backgroundColor: template.colors.accent }}
                  >
                    <Check className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-[#0A1A2F]">{feature.title}</h4>
                    <p className="text-sm text-[#0A1A2F]/70">{feature.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* CTA final */}
          <div className="mt-16 text-center">
            <Button
              onClick={() => navigate("/dashboard")}
              className="bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] text-white hover:shadow-lg rounded-xl px-12 h-14 font-semibold transition-all text-lg"
            >
              Créer ma boutique avec ce template
            </Button>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}

