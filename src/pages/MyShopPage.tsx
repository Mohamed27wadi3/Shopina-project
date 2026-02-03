import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { DashboardHeader } from "../components/DashboardHeader";
import { DashboardSidebar } from "../components/DashboardSidebar";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import { useAPI } from "../hooks/useAPI";
import { 
  CheckCircle, ChevronDown, Package, ShoppingCart, TrendingUp, 
  Star, Settings, Loader2, CreditCard, Palette, MapPin, Globe, Zap
} from "lucide-react";

interface ShopData {
  id: number;
  name: string;
  description: string;
  email: string;
  phone_number: string;
  logo?: string;
  banner_image?: string;
  primary_color?: string;
  secondary_color?: string;
  total_products?: number;
  total_orders?: number;
  total_sales?: number;
  average_rating?: number;
  slug: string;
}

export function MyShopPage() {
  const { user } = useAuth();
  const api = useAPI();
  const location = useLocation();
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [shop, setShop] = useState<ShopData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showSuccessMessage, setShowSuccessMessage] = useState(location.state?.shopCreated || false);
  const [editMode, setEditMode] = useState(false);
  const [expandedSection, setExpandedSection] = useState<string | null>("general");

  const savedTemplate = localStorage.getItem("selectedTemplate");
  const templateData = savedTemplate ? JSON.parse(savedTemplate) : null;

  const [name, setName] = useState(templateData?.components?.storeName || user?.shop_name || "Ma Boutique");
  const [description, setDescription] = useState(templateData?.components?.heroText || "");
  const [email, setEmail] = useState(user?.email || "");
  const [phone, setPhone] = useState(user?.phone_number || "");
  const [logo, setLogo] = useState("");
  const [bannerImage, setBannerImage] = useState("");
  const [primaryColor, setPrimaryColor] = useState("#0077FF");
  const [secondaryColor, setSecondaryColor] = useState("#5AC8FA");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [postalCode, setPostalCode] = useState("");
  const [country, setCountry] = useState("Algérie");
  const [shippingCost, setShippingCost] = useState("0");
  const [freeShippingThreshold, setFreeShippingThreshold] = useState("1000");
  const [acceptsCard, setAcceptsCard] = useState(true);
  const [acceptsBankTransfer, setAcceptsBankTransfer] = useState(true);
  const [acceptsCash, setAcceptsCash] = useState(true);
  const [bankName, setBankName] = useState("");
  const [bankAccount, setBankAccount] = useState("");
  const [metaDescription, setMetaDescription] = useState("");
  const [metaKeywords, setMetaKeywords] = useState("");
  const [instagram, setInstagram] = useState("");
  const [facebook, setFacebook] = useState("");
  const [whatsapp, setWhatsapp] = useState("");
  const [website, setWebsite] = useState("");
  const [currency, setCurrency] = useState("DZD");
  const [timezone, setTimezone] = useState("Africa/Algiers");
  const [returnsPolicy, setReturnsPolicy] = useState("");
  const [termsAndConditions, setTermsAndConditions] = useState("");

  useEffect(() => {
    let ignore = false;
    async function load() {
      try {
        setLoading(true);
        setError(null);
        const res = await api.get('/shop/api/my-shop/');
        if (!ignore) {
          if (res.ok) {
            const data = await res.json();
            setShop(data);
            setName(data.name);
            setDescription(data.description);
            setEmail(data.email);
            setPhone(data.phone_number);
          } else if (res.status !== 404) {
            setError("Impossible de charger votre boutique");
          }
        }
      } catch (err) {
        if (!ignore) setError("Erreur de connexion");
      } finally {
        if (!ignore) setLoading(false);
      }
    }
    load();
    return () => { ignore = true; };
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    try {
      const shopData = {
        name, description, email, phone, logo, banner_image: bannerImage,
        primary_color: primaryColor, secondary_color: secondaryColor,
        address, city, postal_code: postalCode, country, shipping_cost: shippingCost,
        free_shipping_threshold: freeShippingThreshold, accepts_card: acceptsCard,
        accepts_bank_transfer: acceptsBankTransfer, accepts_cash: acceptsCash,
        bank_name: bankName, bank_account: bankAccount, meta_description: metaDescription,
        meta_keywords: metaKeywords, instagram, facebook, whatsapp, website,
        currency, timezone, returns_policy: returnsPolicy, terms_and_conditions: termsAndConditions,
      };
      const res = await api.post('/shop/api/create/', shopData);
      if (res.ok) {
        toast.success("Boutique créée avec succès!");
        setShop(await res.json());
        setEditMode(false);
      } else {
        toast.error("Erreur lors de la création");
      }
    } catch (err) {
      toast.error("Erreur de connexion");
    } finally {
      setCreating(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!shop) return;
    setCreating(true);
    try {
      const shopData = { name, description, email, phone };
      const res = await api.put(`/shop/api/shops/${shop.id}/`, shopData);
      if (res.ok) {
        toast.success("Boutique mise à jour!");
        setShop(await res.json());
        setEditMode(false);
      } else {
        toast.error("Erreur lors de la mise à jour");
      }
    } catch (err) {
      toast.error("Erreur de connexion");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <DashboardHeader />
      <div className="flex">
        <DashboardSidebar />
        <main className="flex-1 p-8 dark:bg-gray-950">
          <div className="mb-8">
            <h1 className="text-[#0A1A2F] dark:text-white mb-2" style={{ fontSize: "36px", fontWeight: "800" }}>
              Ma boutique 🏪
            </h1>
            <p className="text-[#0A1A2F]/60 dark:text-gray-400">Gérez et personnalisez votre boutique en ligne</p>
          </div>

          {showSuccessMessage && (
            <div className="mb-8 p-4 bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500 rounded flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-green-700 dark:text-green-300 font-semibold">Boutique créée avec succès!</p>
                <p className="text-green-600 dark:text-green-400 text-sm">Commencez à ajouter vos produits et à personnaliser votre boutique.</p>
              </div>
            </div>
          )}

          {loading && (
            <div className="flex items-center justify-center py-24">
              <div className="text-center">
                <Loader2 className="w-12 h-12 animate-spin text-[#0077FF] mx-auto mb-4" />
                <p className="text-[#0A1A2F]/60 dark:text-gray-400">Chargement de votre boutique...</p>
              </div>
            </div>
          )}

          {!loading && shop && (
            <div className="space-y-6">
              {/* Shop Overview Card */}
              <Card className="border-2 border-gray-100 dark:border-gray-800 rounded-2xl overflow-hidden">
                <CardHeader className="bg-gradient-to-r from-[#0077FF]/5 to-[#5AC8FA]/5 border-b-2 border-gray-100 dark:border-gray-800">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4">
                      {logo && <img src={logo} alt={shop.name} className="w-16 h-16 rounded-xl object-cover border-2 border-gray-200 dark:border-gray-700" />}
                      <div>
                        <CardTitle className="text-[#0A1A2F] dark:text-white text-2xl">{shop.name}</CardTitle>
                        <p className="text-[#0A1A2F]/60 dark:text-gray-400 text-sm mt-1">Créée par {user?.username}</p>
                      </div>
                    </div>
                    <Button
                      onClick={() => setEditMode(!editMode)}
                      className={`${
                        editMode 
                          ? 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 border-red-200 dark:border-red-800' 
                          : 'bg-[#0077FF] hover:bg-[#0077FF]/90 text-white'
                      } border-2 rounded-xl px-6 py-2 font-semibold transition-all`}
                    >
                      {editMode ? '✕ Annuler' : '✏️ Modifier'}
                    </Button>
                  </div>
                </CardHeader>
                <CardContent className="p-6">
                  <p className="text-[#0A1A2F]/70 dark:text-gray-300 mb-4">{shop.description}</p>
                  {editMode && (
                    <form onSubmit={handleUpdate} className="space-y-4">
                      <div>
                        <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Nom</label>
                        <Input value={name} onChange={(e) => setName(e.target.value)} className="rounded-lg border-2" />
                      </div>
                      <div>
                        <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Description</label>
                        <Textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} className="rounded-lg border-2" />
                      </div>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Email</label>
                          <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="rounded-lg border-2" />
                        </div>
                        <div>
                          <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Téléphone</label>
                          <Input value={phone} onChange={(e) => setPhone(e.target.value)} className="rounded-lg border-2" />
                        </div>
                      </div>
                      <Button type="submit" disabled={creating} className="bg-green-600 hover:bg-green-700 text-white rounded-lg w-full py-2 font-semibold">
                        {creating ? 'Mise à jour...' : 'Enregistrer'}
                      </Button>
                    </form>
                  )}
                </CardContent>
              </Card>

              {/* Stats Grid */}
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                  { title: "Produits", value: shop.total_products ?? 0, icon: Package, color: "text-blue-600" },
                  { title: "Commandes", value: shop.total_orders ?? 0, icon: ShoppingCart, color: "text-purple-600" },
                  { title: "Ventes", value: `${Math.round((shop.total_sales ?? 0) as number)} DZD`, icon: TrendingUp, color: "text-green-600" },
                  { title: "Note", value: `${(shop.average_rating ?? 0).toFixed(1)}/5`, icon: Star, color: "text-yellow-600" },
                ].map((stat) => {
                  const Icon = stat.icon;
                  return (
                    <Card key={stat.title} className="border-2 border-gray-100 dark:border-gray-800 rounded-2xl hover:shadow-lg transition-all">
                      <CardContent className="p-6">
                        <div className="flex items-center justify-between mb-4">
                          <div className={`p-3 rounded-xl bg-gray-100 dark:bg-gray-800 ${stat.color}`}>
                            <Icon className="w-6 h-6" />
                          </div>
                        </div>
                        <p className="text-[#0A1A2F]/60 dark:text-gray-400 text-sm mb-1">{stat.title}</p>
                        <p className="text-[#0A1A2F] dark:text-white text-2xl font-bold">{stat.value}</p>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>

              {/* Quick Actions */}
              <Card className="border-2 border-gray-100 dark:border-gray-800 rounded-2xl">
                <CardHeader>
                  <CardTitle className="text-[#0A1A2F] dark:text-white flex items-center gap-2">
                    <Zap className="w-5 h-5 text-[#0077FF]" />
                    Actions rapides
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {/* Removed 'Tableau de bord' quick-action as requested */}
                    <a href="/dashboard" className="p-4 border-2 border-gray-200 dark:border-gray-700 hover:border-[#0077FF] rounded-xl hover:shadow-lg transition-all group">
                      <Package className="w-6 h-6 text-[#0077FF] mb-2 group-hover:scale-110 transition-transform" />
                      <p className="text-[#0A1A2F] dark:text-white font-semibold">Produits</p>
                      <p className="text-[#0A1A2F]/60 dark:text-gray-400 text-xs">Gérer produits</p>
                    </a>
                    <a href="/orders" className="p-4 border-2 border-gray-200 dark:border-gray-700 hover:border-[#0077FF] rounded-xl hover:shadow-lg transition-all group">
                      <ShoppingCart className="w-6 h-6 text-[#0077FF] mb-2 group-hover:scale-110 transition-transform" />
                      <p className="text-[#0A1A2F] dark:text-white font-semibold">Commandes</p>
                      <p className="text-[#0A1A2F]/60 dark:text-gray-400 text-xs">Voir commandes</p>
                    </a>
                    <a href="/shop/settings/" className="p-4 border-2 border-gray-200 dark:border-gray-700 hover:border-[#0077FF] rounded-xl hover:shadow-lg transition-all group">
                      <Settings className="w-6 h-6 text-[#0077FF] mb-2 group-hover:scale-110 transition-transform" />
                      <p className="text-[#0A1A2F] dark:text-white font-semibold">Paramètres</p>
                      <p className="text-[#0A1A2F]/60 dark:text-gray-400 text-xs">Configurez</p>
                    </a>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {!loading && !shop && !error && (
            <div className="space-y-8">
              {/* Create Shop CTA */}
              <Card className="border-2 border-[#0077FF]/30 rounded-2xl overflow-hidden bg-gradient-to-br from-[#0077FF]/5 to-[#5AC8FA]/5">
                <CardContent className="p-12 text-center">
                  <div className="text-5xl mb-4">🏪</div>
                  <h2 className="text-3xl font-bold text-[#0A1A2F] dark:text-white mb-3">Créer votre boutique</h2>
                  <p className="text-[#0A1A2F]/60 dark:text-gray-400 max-w-2xl mx-auto mb-8">
                    Lancez votre activité e-commerce en quelques minutes. Remplissez le formulaire pour créer votre boutique.
                  </p>
                </CardContent>
              </Card>

              {/* Create Form */}
              <form onSubmit={handleCreate} className="space-y-6 max-w-4xl mx-auto">
                {/* General Section */}
                <Card className="border-2 border-gray-100 dark:border-gray-800 rounded-2xl overflow-hidden">
                  <button
                    type="button"
                    onClick={() => setExpandedSection(expandedSection === 'general' ? null : 'general')}
                    className="w-full flex items-center gap-3 p-4 bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all border-b-2 border-gray-100 dark:border-gray-800"
                  >
                    <div className="text-2xl">📝</div>
                    <div className="text-left flex-1">
                      <p className="font-semibold text-[#0A1A2F] dark:text-white">Informations générales</p>
                      <p className="text-xs text-[#0A1A2F]/60 dark:text-gray-400">Nom, description, contact</p>
                    </div>
                    <ChevronDown className={`w-5 h-5 transition-transform ${expandedSection === 'general' ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedSection === 'general' && (
                    <CardContent className="p-6 space-y-4">
                      <div>
                        <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Nom de la boutique *</label>
                        <Input value={name} onChange={(e) => setName(e.target.value)} required placeholder="Ex: Mon Magasin" className="rounded-lg" />
                      </div>
                      <div>
                        <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Description *</label>
                        <Textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} placeholder="Décrivez votre boutique..." className="rounded-lg" />
                      </div>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Email *</label>
                          <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="contact@shop.com" className="rounded-lg" />
                        </div>
                        <div>
                          <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Téléphone *</label>
                          <Input value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="+213..." className="rounded-lg" />
                        </div>
                      </div>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Devise</label>
                          <select value={currency} onChange={(e) => setCurrency(e.target.value)} className="w-full h-10 rounded-lg border-2 border-gray-200 dark:border-gray-700 px-3">
                            <option>DZD</option><option>USD</option><option>EUR</option>
                          </select>
                        </div>
                        <div>
                          <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Fuseau horaire</label>
                          <select value={timezone} onChange={(e) => setTimezone(e.target.value)} className="w-full h-10 rounded-lg border-2 border-gray-200 dark:border-gray-700 px-3">
                            <option>Africa/Algiers</option><option>Europe/Paris</option>
                          </select>
                        </div>
                      </div>
                    </CardContent>
                  )}
                </Card>

                {/* Branding Section */}
                <Card className="border-2 border-gray-100 dark:border-gray-800 rounded-2xl overflow-hidden">
                  <button
                    type="button"
                    onClick={() => setExpandedSection(expandedSection === 'branding' ? null : 'branding')}
                    className="w-full flex items-center gap-3 p-4 bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all border-b-2 border-gray-100 dark:border-gray-800"
                  >
                    <div className="text-2xl">🎨</div>
                    <div className="text-left flex-1">
                      <p className="font-semibold text-[#0A1A2F] dark:text-white">Branding & Design</p>
                      <p className="text-xs text-[#0A1A2F]/60 dark:text-gray-400">Logo, couleurs, bannière</p>
                    </div>
                    <ChevronDown className={`w-5 h-5 transition-transform ${expandedSection === 'branding' ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedSection === 'branding' && (
                    <CardContent className="p-6 space-y-4">
                      <div>
                        <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">URL du logo</label>
                        <Input value={logo} onChange={(e) => setLogo(e.target.value)} placeholder="https://..." className="rounded-lg" />
                      </div>
                      <div>
                        <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">URL de la bannière</label>
                        <Input value={bannerImage} onChange={(e) => setBannerImage(e.target.value)} placeholder="https://..." className="rounded-lg" />
                      </div>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Couleur primaire</label>
                          <div className="flex gap-2">
                            <input type="color" value={primaryColor} onChange={(e) => setPrimaryColor(e.target.value)} className="w-12 h-10 rounded-lg cursor-pointer border-2 border-gray-200 dark:border-gray-700" />
                            <Input value={primaryColor} onChange={(e) => setPrimaryColor(e.target.value)} className="rounded-lg flex-1" />
                          </div>
                        </div>
                        <div>
                          <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Couleur secondaire</label>
                          <div className="flex gap-2">
                            <input type="color" value={secondaryColor} onChange={(e) => setSecondaryColor(e.target.value)} className="w-12 h-10 rounded-lg cursor-pointer border-2 border-gray-200 dark:border-gray-700" />
                            <Input value={secondaryColor} onChange={(e) => setSecondaryColor(e.target.value)} className="rounded-lg flex-1" />
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  )}
                </Card>

                {/* Shipping Section */}
                <Card className="border-2 border-gray-100 dark:border-gray-800 rounded-2xl overflow-hidden">
                  <button
                    type="button"
                    onClick={() => setExpandedSection(expandedSection === 'shipping' ? null : 'shipping')}
                    className="w-full flex items-center gap-3 p-4 bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all border-b-2 border-gray-100 dark:border-gray-800"
                  >
                    <div className="text-2xl">📦</div>
                    <div className="text-left flex-1">
                      <p className="font-semibold text-[#0A1A2F] dark:text-white">Adresse & Livraison</p>
                      <p className="text-xs text-[#0A1A2F]/60 dark:text-gray-400">Lieu, tarifs de livraison</p>
                    </div>
                    <ChevronDown className={`w-5 h-5 transition-transform ${expandedSection === 'shipping' ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedSection === 'shipping' && (
                    <CardContent className="p-6 space-y-4">
                      <div>
                        <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Adresse</label>
                        <Input value={address} onChange={(e) => setAddress(e.target.value)} placeholder="123 Rue..." className="rounded-lg" />
                      </div>
                      <div className="grid md:grid-cols-3 gap-4">
                        <Input value={city} onChange={(e) => setCity(e.target.value)} placeholder="Ville" className="rounded-lg" />
                        <Input value={postalCode} onChange={(e) => setPostalCode(e.target.value)} placeholder="Code postal" className="rounded-lg" />
                        <select value={country} onChange={(e) => setCountry(e.target.value)} className="h-10 rounded-lg border-2 border-gray-200 dark:border-gray-700 px-3">
                          <option>Algérie</option><option>France</option><option>Tunisie</option><option>Maroc</option>
                        </select>
                      </div>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Coût livraison (DZD)</label>
                          <Input type="number" value={shippingCost} onChange={(e) => setShippingCost(e.target.value)} placeholder="0" className="rounded-lg" />
                        </div>
                        <div>
                          <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Gratuit à partir de (DZD)</label>
                          <Input type="number" value={freeShippingThreshold} onChange={(e) => setFreeShippingThreshold(e.target.value)} placeholder="1000" className="rounded-lg" />
                        </div>
                      </div>
                    </CardContent>
                  )}
                </Card>

                {/* Payment Section */}
                <Card className="border-2 border-gray-100 dark:border-gray-800 rounded-2xl overflow-hidden">
                  <button
                    type="button"
                    onClick={() => setExpandedSection(expandedSection === 'payment' ? null : 'payment')}
                    className="w-full flex items-center gap-3 p-4 bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all border-b-2 border-gray-100 dark:border-gray-800"
                  >
                    <div className="text-2xl">💳</div>
                    <div className="text-left flex-1">
                      <p className="font-semibold text-[#0A1A2F] dark:text-white">Paramètres de paiement</p>
                      <p className="text-xs text-[#0A1A2F]/60 dark:text-gray-400">Modes de paiement acceptés</p>
                    </div>
                    <ChevronDown className={`w-5 h-5 transition-transform ${expandedSection === 'payment' ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedSection === 'payment' && (
                    <CardContent className="p-6 space-y-4">
                      <label className="flex items-center gap-3 p-3 hover:bg-gray-50 dark:hover:bg-gray-800/50 rounded-lg cursor-pointer">
                        <input type="checkbox" checked={acceptsCard} onChange={(e) => setAcceptsCard(e.target.checked)} className="w-5 h-5 rounded" />
                        <span className="font-semibold text-[#0A1A2F] dark:text-white">💳 Cartes bancaires</span>
                      </label>
                      <label className="flex items-center gap-3 p-3 hover:bg-gray-50 dark:hover:bg-gray-800/50 rounded-lg cursor-pointer">
                        <input type="checkbox" checked={acceptsBankTransfer} onChange={(e) => setAcceptsBankTransfer(e.target.checked)} className="w-5 h-5 rounded" />
                        <span className="font-semibold text-[#0A1A2F] dark:text-white">🏦 Virements bancaires</span>
                      </label>
                      <label className="flex items-center gap-3 p-3 hover:bg-gray-50 dark:hover:bg-gray-800/50 rounded-lg cursor-pointer">
                        <input type="checkbox" checked={acceptsCash} onChange={(e) => setAcceptsCash(e.target.checked)} className="w-5 h-5 rounded" />
                        <span className="font-semibold text-[#0A1A2F] dark:text-white">💰 Paiement à la livraison</span>
                      </label>
                      {acceptsBankTransfer && (
                        <>
                          <div>
                            <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Banque</label>
                            <Input value={bankName} onChange={(e) => setBankName(e.target.value)} placeholder="Nom de la banque" className="rounded-lg" />
                          </div>
                          <div>
                            <label className="text-sm font-semibold text-[#0A1A2F] dark:text-gray-300 block mb-2">Compte bancaire</label>
                            <Input value={bankAccount} onChange={(e) => setBankAccount(e.target.value)} placeholder="IBAN / RIB" className="rounded-lg" />
                          </div>
                        </>
                      )}
                    </CardContent>
                  )}
                </Card>

                {/* Social Section */}
                <Card className="border-2 border-gray-100 dark:border-gray-800 rounded-2xl overflow-hidden">
                  <button
                    type="button"
                    onClick={() => setExpandedSection(expandedSection === 'social' ? null : 'social')}
                    className="w-full flex items-center gap-3 p-4 bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all border-b-2 border-gray-100 dark:border-gray-800"
                  >
                    <div className="text-2xl">🌐</div>
                    <div className="text-left flex-1">
                      <p className="font-semibold text-[#0A1A2F] dark:text-white">Réseaux sociaux & Contact</p>
                      <p className="text-xs text-[#0A1A2F]/60 dark:text-gray-400">Connectez vos profils</p>
                    </div>
                    <ChevronDown className={`w-5 h-5 transition-transform ${expandedSection === 'social' ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedSection === 'social' && (
                    <CardContent className="p-6 space-y-4">
                      <div className="grid md:grid-cols-2 gap-4">
                        <Input value={instagram} onChange={(e) => setInstagram(e.target.value)} placeholder="📸 Instagram @..." className="rounded-lg" />
                        <Input value={facebook} onChange={(e) => setFacebook(e.target.value)} placeholder="f Facebook" className="rounded-lg" />
                        <Input value={whatsapp} onChange={(e) => setWhatsapp(e.target.value)} placeholder="💬 WhatsApp +213..." className="rounded-lg" />
                        <Input value={website} onChange={(e) => setWebsite(e.target.value)} placeholder="🌍 Site web https://..." className="rounded-lg" />
                      </div>
                    </CardContent>
                  )}
                </Card>

                {/* Submit Button */}
                <div className="flex gap-4 justify-center pt-4">
                  <Button type="submit" disabled={creating} className="bg-green-600 hover:bg-green-700 text-white rounded-xl px-12 py-3 font-semibold transition-all hover:shadow-lg">
                    {creating ? '⏳ Création en cours...' : '🚀 Créer ma boutique'}
                  </Button>
                  <Link to="/dashboard" className="bg-gray-400 hover:bg-gray-500 text-white rounded-xl px-8 py-3 font-semibold transition-all">
                    ← Retour
                  </Link>
                </div>
              </form>
            </div>
          )}

          {!loading && error && (
            <Card className="border-2 border-red-200 dark:border-red-800 rounded-2xl bg-red-50 dark:bg-red-900/20">
              <CardContent className="p-6">
                <p className="text-red-700 dark:text-red-400 font-semibold mb-2">⚠️ Erreur:</p>
                <p className="text-red-600 dark:text-red-300 mb-4">{error}</p>
                <p className="text-red-600 dark:text-red-300 text-sm">Créez une nouvelle boutique ci-dessous.</p>
              </CardContent>
            </Card>
          )}
        </main>
      </div>
    </div>
  );
}
