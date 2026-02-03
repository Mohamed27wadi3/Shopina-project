import { useEffect, useMemo, useState } from "react";
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
import { CheckCircle, ChevronDown, Globe, MapPin, CreditCard, Package, Zap, Store, TrendingUp, ShoppingCart, Star, Settings, Plus } from "lucide-react";

export function MyShopPage() {
  console.log('🎯 MyShopPage mounted');
  
  const { user } = useAuth();
  const api = useAPI();
  const location = useLocation();
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [shop, setShop] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showSuccessMessage, setShowSuccessMessage] = useState(location.state?.shopCreated || false);

  // Initialiser avec les données du template si disponibles
  const savedTemplate = localStorage.getItem("selectedTemplate");
  const templateData = savedTemplate ? JSON.parse(savedTemplate) : null;

  const [name, setName] = useState(templateData?.components?.storeName || user?.shop_name || "Ma Boutique");
  const [description, setDescription] = useState(templateData?.components?.heroText || "Commencez à vendre dès aujourd'hui avec Shopina");
  const [email, setEmail] = useState(user?.email || "");
  const [phone, setPhone] = useState(user?.phone_number || "");
  
  // Branding options
  const [logo, setLogo] = useState("");
  const [bannerImage, setBannerImage] = useState("");
  const [primaryColor, setPrimaryColor] = useState("#0077FF");
  const [secondaryColor, setSecondaryColor] = useState("#5AC8FA");
  
  // Paramètres de livraison
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [postalCode, setPostalCode] = useState("");
  const [country, setCountry] = useState("Algérie");
  const [shippingCost, setShippingCost] = useState("0");
  const [freeShippingThreshold, setFreeShippingThreshold] = useState("1000");
  
  // Paramètres de paiement
  const [acceptsCard, setAcceptsCard] = useState(true);
  const [acceptsBankTransfer, setAcceptsBankTransfer] = useState(true);
  const [acceptsCash, setAcceptsCash] = useState(true);
  const [bankName, setBankName] = useState("");
  const [bankAccount, setBankAccount] = useState("");
  
  // Paramètres SEO
  const [metaDescription, setMetaDescription] = useState("");
  const [metaKeywords, setMetaKeywords] = useState("");
  
  // Paramètres de contact
  const [instagram, setInstagram] = useState("");
  const [facebook, setFacebook] = useState("");
  const [whatsapp, setWhatsapp] = useState("");
  const [website, setWebsite] = useState("");
  
  // Paramètres généraux
  const [currency, setCurrency] = useState("DZD");
  const [timezone, setTimezone] = useState("Africa/Algiers");
  const [returnsPolicy, setReturnsPolicy] = useState("");
  const [termsAndConditions, setTermsAndConditions] = useState("");
  
  // UI State
  const [expandedSection, setExpandedSection] = useState<string | null>("general");
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    let ignore = false;
    let hasLoaded = false;
    
    async function load() {
      if (hasLoaded || loading === false) return;
      hasLoaded = true;
      
      console.log('🔄 Loading shop data...');
      setLoading(true);
      setError(null);
      try {
        console.log('📡 Calling /shop/api/my-shop/');
        const res = await api.get('/shop/api/my-shop/');
        
        console.log('📊 Response status:', res.status);
        
        if (!ignore) {
          if (res.ok) {
            const data = await res.json();
            console.log('✅ Shop loaded:', data);
            setShop(data);
          } else if (res.status === 404) {
            console.log('📭 No shop found yet (404)');
            setShop(null);
          } else {
            const text = await res.text();
            console.error('❌ Error loading shop:', res.status, text);
            setError(`Erreur ${res.status}: ${text || "Erreur serveur"}`);
          }
        }
      } catch (e: any) {
        if (!ignore) {
          console.error('❌ Exception in load:', e);
          setError(e?.message || "Erreur réseau - Vérifiez que le backend est lancé");
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }
    
    load();
    return () => { ignore = true; };
  }, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreating(true);
    try {
      const shopData = {
        name, description, email, phone,
        logo, bannerImage, primaryColor, secondaryColor,
        address, city, postalCode, country,
        shippingCost: parseFloat(shippingCost),
        freeShippingThreshold: parseFloat(freeShippingThreshold),
        acceptsCard, acceptsBankTransfer, acceptsCash,
        bankName, bankAccount,
        metaDescription, metaKeywords,
        instagram, facebook, whatsapp, website,
        currency, timezone, returnsPolicy, termsAndConditions
      };
      
      const res = await api.post('/shop/api/create/', shopData);

      if (res.ok) {
        const data = await res.json();
        console.log('✅ Shop created:', data);
        toast.success('Boutique créée avec succès');
        setShop(data);
        setEditMode(false);
      } else {
        const data = await res.json().catch(() => ({}));
        const msg = data?.detail || Object.values(data || {}).flat().join(" \n ") || 'Erreur lors de la création';
        console.error('❌ Error creating shop:', msg);
        toast.error(msg);
      }
    } catch (e: any) {
      console.error('❌ Exception in handleCreate:', e);
      toast.error(e?.message || 'Erreur réseau');
    } finally {
      setCreating(false);
    }
  }
  
  async function handleUpdate(e: React.FormEvent) {
    e.preventDefault();
    if (!shop) return;
    setCreating(true);
    try {
      const shopData = {
        name, description, email, phone,
        logo, bannerImage, primaryColor, secondaryColor,
        address, city, postalCode, country,
        shippingCost: parseFloat(shippingCost),
        freeShippingThreshold: parseFloat(freeShippingThreshold),
        acceptsCard, acceptsBankTransfer, acceptsCash,
        bankName, bankAccount,
        metaDescription, metaKeywords,
        instagram, facebook, whatsapp, website,
        currency, timezone, returnsPolicy, termsAndConditions
      };
      
      const res = await api.put(`/shop/api/shops/${shop.id}/`, shopData);

      if (res.ok) {
        const data = await res.json();
        console.log('✅ Shop updated:', data);
        toast.success('Boutique mise à jour avec succès');
        setShop(data);
        setEditMode(false);
      } else {
        const data = await res.json().catch(() => ({}));
        const msg = data?.detail || Object.values(data || {}).flat().join(" \n ") || 'Erreur lors de la mise à jour';
        console.error('❌ Error updating shop:', msg);
        toast.error(msg);
      }
    } catch (e: any) {
      console.error('❌ Exception in handleUpdate:', e);
      toast.error(e?.message || 'Erreur réseau');
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <DashboardHeader />
      <div className="flex">
        <DashboardSidebar />

        <main className="flex-1 p-8 dark:bg-gray-950">
          {/* Success Message */}
          {showSuccessMessage && (
            <div className="mb-8 p-6 bg-gradient-to-r from-green-500/20 to-emerald-500/20 border-2 border-green-500/50 rounded-2xl flex items-start gap-4 animate-pulse">
              <CheckCircle className="w-7 h-7 text-green-400 flex-shrink-0 mt-1" />
              <div className="flex-1">
                <h3 className="font-bold text-green-300 mb-1 text-lg">🎉 Boutique créée avec succès!</h3>
                <p className="text-green-200 text-sm">Votre boutique a été créée à partir du template. Commencez à la personnaliser et ajouter vos produits!</p>
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex flex-col items-center justify-center py-32 space-y-4">
              <div className="relative w-16 h-16">
                <div className="absolute inset-0 bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] rounded-full animate-spin"></div>
                <div className="absolute inset-2 bg-[#0A1A2F] rounded-full"></div>
              </div>
              <p className="text-xl font-semibold text-[#5AC8FA]">Chargement de votre boutique...</p>
              <p className="text-white/60">Veuillez patienter quelques instants</p>
            </div>
          )}

          {/* Error State */}
          {!loading && error && (
            <div className="mb-8 p-6 bg-gradient-to-r from-red-500/20 to-pink-500/20 border-2 border-red-500/50 rounded-2xl">
              <p className="text-red-300 font-semibold mb-2">⚠️ Problème lors du chargement :</p>
              <p className="text-red-200 text-sm mb-4">{error}</p>
            </div>
          )}

          {/* Has Shop: Dashboard */}
          {!loading && !error && shop && (
            <div className="space-y-8">
              {/* Shop Header Card */}
              <div className="bg-gradient-to-br from-[#0077FF]/20 to-[#5AC8FA]/20 border-2 border-[#0077FF]/50 rounded-3xl p-8 backdrop-blur">
                <div className="flex items-start justify-between gap-6">
                  <div>
                    <div className="flex items-center gap-3 mb-3">
                      {logo && <img src={logo} alt="Logo" className="w-16 h-16 rounded-xl object-cover border-2 border-[#5AC8FA]" />}
                      <div>
                        <h2 className="text-4xl font-black text-white">{shop.name}</h2>
                        <p className="text-[#5AC8FA] font-semibold">Votre boutique en ligne</p>
                      </div>
                    </div>
                    <p className="text-white/80 mt-4 max-w-2xl">{shop.description}</p>
                  </div>
                  <Button 
                    onClick={() => setEditMode(!editMode)}
                    className={`${editMode ? 'bg-red-500 hover:bg-red-600' : 'bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] hover:from-[#0077FF]/90 hover:to-[#5AC8FA]/90'} text-white rounded-xl px-6 py-3 font-bold flex items-center gap-2 whitespace-nowrap`}
                  >
                    {editMode ? '✕ Annuler' : '✏️ Modifier'}
                  </Button>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/10 border-2 border-blue-500/30 rounded-2xl p-6 hover:shadow-2xl transition-all hover:scale-105 cursor-pointer">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 bg-blue-500/30 rounded-xl">
                      <Package className="w-6 h-6 text-blue-300" />
                    </div>
                    <span className="text-blue-300 text-xs font-bold">📈</span>
                  </div>
                  <p className="text-white/70 text-sm mb-1">Produits</p>
                  <p className="text-3xl font-black text-blue-300">{shop.total_products ?? 0}</p>
                </div>

                <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/10 border-2 border-purple-500/30 rounded-2xl p-6 hover:shadow-2xl transition-all hover:scale-105 cursor-pointer">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 bg-purple-500/30 rounded-xl">
                      <ShoppingCart className="w-6 h-6 text-purple-300" />
                    </div>
                    <span className="text-purple-300 text-xs font-bold">🔥</span>
                  </div>
                  <p className="text-white/70 text-sm mb-1">Commandes</p>
                  <p className="text-3xl font-black text-purple-300">{shop.total_orders ?? 0}</p>
                </div>

                <div className="bg-gradient-to-br from-green-500/20 to-green-600/10 border-2 border-green-500/30 rounded-2xl p-6 hover:shadow-2xl transition-all hover:scale-105 cursor-pointer">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 bg-green-500/30 rounded-xl">
                      <TrendingUp className="w-6 h-6 text-green-300" />
                    </div>
                    <span className="text-green-300 text-xs font-bold">💰</span>
                  </div>
                  <p className="text-white/70 text-sm mb-1">Ventes</p>
                  <p className="text-3xl font-black text-green-300">{Math.round((shop.total_sales ?? 0) as number)} DZD</p>
                </div>

                <div className="bg-gradient-to-br from-yellow-500/20 to-yellow-600/10 border-2 border-yellow-500/30 rounded-2xl p-6 hover:shadow-2xl transition-all hover:scale-105 cursor-pointer">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 bg-yellow-500/30 rounded-xl">
                      <Star className="w-6 h-6 text-yellow-300" />
                    </div>
                    <span className="text-yellow-300 text-xs font-bold">⭐</span>
                  </div>
                  <p className="text-white/70 text-sm mb-1">Note moyenne</p>
                  <p className="text-3xl font-black text-yellow-300">{(shop.average_rating ?? 0).toFixed(1)}/5</p>
                </div>
              </div>

              {/* Edit Mode */}
              {editMode && (
                <div className="bg-gradient-to-br from-[#0077FF]/10 to-[#5AC8FA]/10 border-2 border-[#0077FF]/50 rounded-2xl p-8">
                  <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                    <span className="bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] px-4 py-2 rounded-xl">✨</span>
                    Modifier votre boutique
                  </h3>
                  <form onSubmit={handleUpdate} className="space-y-6 max-w-3xl">
                    <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Nom</label>
                      <Input value={name} onChange={e => setName(e.target.value)} className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white placeholder-white/50 focus:border-[#5AC8FA]" /></div>
                    <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Description</label>
                      <Textarea value={description} onChange={e => setDescription(e.target.value)} rows={4} className="rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white placeholder-white/50 focus:border-[#5AC8FA]" /></div>
                    <div className="grid md:grid-cols-2 gap-6">
                      <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Email</label>
                        <Input type="email" value={email} onChange={e => setEmail(e.target.value)} className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white placeholder-white/50 focus:border-[#5AC8FA]" /></div>
                      <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Téléphone</label>
                        <Input value={phone} onChange={e => setPhone(e.target.value)} className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white placeholder-white/50 focus:border-[#5AC8FA]" /></div>
                    </div>
                    <div className="flex gap-3">
                      <Button type="submit" disabled={creating} className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white rounded-xl px-8 py-3 font-bold">
                        {creating ? '⏳ Mise à jour...' : '💾 Enregistrer'}
                      </Button>
                    </div>
                  </form>
                </div>
              )}

              {/* Quick Actions */}
              {!editMode && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <a href={`/shop/${shop.slug}/dashboard/`} className="group bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded-2xl p-6 text-center transition-all hover:shadow-2xl hover:scale-105">
                    <div className="text-3xl mb-2 group-hover:scale-110 transition-transform">📊</div>
                    <div className="font-bold">Tableau de bord</div>
                    <div className="text-white/80 text-sm">Voir les statistiques</div>
                  </a>
                  <a href="/dashboard" className="group bg-gradient-to-br from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white rounded-2xl p-6 text-center transition-all hover:shadow-2xl hover:scale-105">
                    <div className="text-3xl mb-2 group-hover:scale-110 transition-transform">📦</div>
                    <div className="font-bold">Ajouter produits</div>
                    <div className="text-white/80 text-sm">Gérer votre catalogue</div>
                  </a>
                  <a href="/orders" className="group bg-gradient-to-br from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white rounded-2xl p-6 text-center transition-all hover:shadow-2xl hover:scale-105">
                    <div className="text-3xl mb-2 group-hover:scale-110 transition-transform">🛒</div>
                    <div className="font-bold">Commandes</div>
                    <div className="text-white/80 text-sm">Voir les commandes</div>
                  </a>
                  <a href="/shop/settings/" className="group bg-gradient-to-br from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white rounded-2xl p-6 text-center transition-all hover:shadow-2xl hover:scale-105">
                    <div className="text-3xl mb-2 group-hover:scale-110 transition-transform">⚙️</div>
                    <div className="font-bold">Paramètres</div>
                    <div className="text-white/80 text-sm">Configurer</div>
                  </a>
                </div>
              )}

              {/* Template Info */}
              {templateData && (
                <div className="bg-gradient-to-r from-[#0077FF]/10 to-[#5AC8FA]/10 border-2 border-[#0077FF]/50 rounded-2xl p-6">
                  <div className="flex items-center gap-4">
                    <div className="text-4xl">📋</div>
                    <div className="flex-1">
                      <p className="text-[#5AC8FA] font-bold text-sm">Template utilisé</p>
                      <h3 className="text-xl font-bold text-white">{templateData.title}</h3>
                      <p className="text-white/70 text-sm">{templateData.category}</p>
                    </div>
                    <Link to="/templates" className="bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] hover:from-[#0077FF]/90 hover:to-[#5AC8FA]/90 text-white rounded-xl px-6 py-3 font-bold transition-all hover:shadow-xl">
                      Voir templates
                    </Link>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* No Shop: Create Form */}
          {!loading && (!shop || error) && (
            <div className="space-y-8">
              <div className="bg-gradient-to-br from-[#0077FF]/20 to-[#5AC8FA]/20 border-2 border-[#0077FF]/50 rounded-3xl p-10 backdrop-blur text-center">
                <div className="text-6xl mb-4">🏪</div>
                <h2 className="text-4xl font-black mb-3">Créer votre boutique</h2>
                <p className="text-white/80 text-lg max-w-2xl mx-auto">Lancez votre activité e-commerce en quelques minutes. Remplissez les formulaires ci-dessous pour commencer!</p>
              </div>

              {error && (
                <div className="p-6 bg-orange-500/20 border-2 border-orange-500/50 rounded-2xl">
                  <p className="text-orange-300 font-semibold mb-2">⚠️ Note :</p>
                  <p className="text-orange-200 text-sm mb-3">{error}</p>
                  <p className="text-orange-200 text-sm">Créez une nouvelle boutique ci-dessous :</p>
                </div>
              )}

              <form onSubmit={handleCreate} className="space-y-6 max-w-4xl mx-auto">
                {/* SECTION: Infos Générales */}
                <div className="bg-gradient-to-br from-[#0077FF]/10 to-[#5AC8FA]/10 border-2 border-[#0077FF]/50 rounded-2xl overflow-hidden hover:shadow-2xl transition-all">
                  <button
                    type="button"
                    onClick={() => setExpandedSection(expandedSection === 'general' ? null : 'general')}
                    className="w-full flex items-center gap-4 p-6 bg-gradient-to-r from-[#0077FF]/20 to-[#5AC8FA]/20 hover:from-[#0077FF]/30 hover:to-[#5AC8FA]/30 transition-all"
                  >
                    <div className="text-3xl">🏢</div>
                    <div className="text-left flex-1">
                      <span className="font-bold text-lg">Informations générales</span>
                      <p className="text-white/60 text-sm">Nom, description, contact</p>
                    </div>
                    <ChevronDown className={`w-6 h-6 transition-transform ${expandedSection === 'general' ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedSection === 'general' && (
                    <div className="p-6 space-y-4 border-t-2 border-[#0077FF]/50">
                      <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Nom de la boutique *</label>
                        <Input value={name} onChange={e => setName(e.target.value)} required placeholder="Ex: Mon Magasin" className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white placeholder-white/50" /></div>
                      <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Description *</label>
                        <Textarea value={description} onChange={e => setDescription(e.target.value)} rows={4} placeholder="Décrivez votre boutique..." className="rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white placeholder-white/50" /></div>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Email *</label>
                          <Input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="contact@shop.com" className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white placeholder-white/50" /></div>
                        <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Téléphone *</label>
                          <Input value={phone} onChange={e => setPhone(e.target.value)} placeholder="+213..." className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white placeholder-white/50" /></div>
                      </div>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Devise</label>
                          <select value={currency} onChange={e => setCurrency(e.target.value)} className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white px-4">
                            <option className="bg-[#0A1A2F]">DZD</option><option className="bg-[#0A1A2F]">USD</option><option className="bg-[#0A1A2F]">EUR</option>
                          </select></div>
                        <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Fuseau horaire</label>
                          <select value={timezone} onChange={e => setTimezone(e.target.value)} className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white px-4">
                            <option className="bg-[#0A1A2F]">Africa/Algiers</option><option className="bg-[#0A1A2F]">Europe/Paris</option>
                          </select></div>
                      </div>
                    </div>
                  )}
                </div>

                {/* SECTION: Branding */}
                <div className="bg-gradient-to-br from-[#5AC8FA]/10 to-[#50E3C2]/10 border-2 border-[#5AC8FA]/50 rounded-2xl overflow-hidden hover:shadow-2xl transition-all">
                  <button
                    type="button"
                    onClick={() => setExpandedSection(expandedSection === 'branding' ? null : 'branding')}
                    className="w-full flex items-center gap-4 p-6 bg-gradient-to-r from-[#5AC8FA]/20 to-[#50E3C2]/20 hover:from-[#5AC8FA]/30 hover:to-[#50E3C2]/30 transition-all"
                  >
                    <div className="text-3xl">🎨</div>
                    <div className="text-left flex-1">
                      <span className="font-bold text-lg">Branding & Design</span>
                      <p className="text-white/60 text-sm">Logo, couleurs, bannière</p>
                    </div>
                    <ChevronDown className={`w-6 h-6 transition-transform ${expandedSection === 'branding' ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedSection === 'branding' && (
                    <div className="p-6 space-y-4 border-t-2 border-[#5AC8FA]/50">
                      <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">URL du logo</label>
                        <Input value={logo} onChange={e => setLogo(e.target.value)} placeholder="https://..." className="h-12 rounded-xl border-2 border-[#5AC8FA]/50 bg-white/10 text-white placeholder-white/50" /></div>
                      <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">URL de la bannière</label>
                        <Input value={bannerImage} onChange={e => setBannerImage(e.target.value)} placeholder="https://..." className="h-12 rounded-xl border-2 border-[#5AC8FA]/50 bg-white/10 text-white placeholder-white/50" /></div>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Couleur primaire</label>
                          <div className="flex gap-3">
                            <input type="color" value={primaryColor} onChange={e => setPrimaryColor(e.target.value)} className="w-16 h-12 rounded-xl border-2 border-[#5AC8FA]/50 cursor-pointer" />
                            <Input value={primaryColor} onChange={e => setPrimaryColor(e.target.value)} className="h-12 rounded-xl border-2 border-[#5AC8FA]/50 bg-white/10 text-white flex-1" /></div></div>
                        <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Couleur secondaire</label>
                          <div className="flex gap-3">
                            <input type="color" value={secondaryColor} onChange={e => setSecondaryColor(e.target.value)} className="w-16 h-12 rounded-xl border-2 border-[#5AC8FA]/50 cursor-pointer" />
                            <Input value={secondaryColor} onChange={e => setSecondaryColor(e.target.value)} className="h-12 rounded-xl border-2 border-[#5AC8FA]/50 bg-white/10 text-white flex-1" /></div></div>
                      </div>
                    </div>
                  )}
                </div>

                {/* SECTION: Livraison */}
                <div className="bg-gradient-to-br from-[#50E3C2]/10 to-[#F5A623]/10 border-2 border-[#50E3C2]/50 rounded-2xl overflow-hidden hover:shadow-2xl transition-all">
                  <button
                    type="button"
                    onClick={() => setExpandedSection(expandedSection === 'shipping' ? null : 'shipping')}
                    className="w-full flex items-center gap-4 p-6 bg-gradient-to-r from-[#50E3C2]/20 to-[#F5A623]/20 hover:from-[#50E3C2]/30 hover:to-[#F5A623]/30 transition-all"
                  >
                    <div className="text-3xl">📦</div>
                    <div className="text-left flex-1">
                      <span className="font-bold text-lg">Adresse & Livraison</span>
                      <p className="text-white/60 text-sm">Lieu, tarifs de livraison</p>
                    </div>
                    <ChevronDown className={`w-6 h-6 transition-transform ${expandedSection === 'shipping' ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedSection === 'shipping' && (
                    <div className="p-6 space-y-4 border-t-2 border-[#50E3C2]/50">
                      <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Adresse</label>
                        <Input value={address} onChange={e => setAddress(e.target.value)} placeholder="123 Rue..." className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white placeholder-white/50" /></div>
                      <div className="grid md:grid-cols-3 gap-4">
                        <div><Input value={city} onChange={e => setCity(e.target.value)} placeholder="Ville" className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white placeholder-white/50" /></div>
                        <div><Input value={postalCode} onChange={e => setPostalCode(e.target.value)} placeholder="Code postal" className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white placeholder-white/50" /></div>
                        <div><select value={country} onChange={e => setCountry(e.target.value)} className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white px-4">
                          <option className="bg-[#0A1A2F]">Algérie</option><option className="bg-[#0A1A2F]">France</option><option className="bg-[#0A1A2F]">Tunisie</option><option className="bg-[#0A1A2F]">Maroc</option>
                        </select></div>
                      </div>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Coût livraison (DZD)</label>
                          <Input type="number" value={shippingCost} onChange={e => setShippingCost(e.target.value)} placeholder="0" className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white placeholder-white/50" /></div>
                        <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Gratuit à partir de (DZD)</label>
                          <Input type="number" value={freeShippingThreshold} onChange={e => setFreeShippingThreshold(e.target.value)} placeholder="1000" className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white placeholder-white/50" /></div>
                      </div>
                    </div>
                  )}
                </div>

                {/* SECTION: Paiement */}
                <div className="bg-gradient-to-br from-[#F5A623]/10 to-[#7ED321]/10 border-2 border-[#F5A623]/50 rounded-2xl overflow-hidden hover:shadow-2xl transition-all">
                  <button
                    type="button"
                    onClick={() => setExpandedSection(expandedSection === 'payment' ? null : 'payment')}
                    className="w-full flex items-center gap-4 p-6 bg-gradient-to-r from-[#F5A623]/20 to-[#7ED321]/20 hover:from-[#F5A623]/30 hover:to-[#7ED321]/30 transition-all"
                  >
                    <div className="text-3xl">💳</div>
                    <div className="text-left flex-1">
                      <span className="font-bold text-lg">Paramètres de paiement</span>
                      <p className="text-white/60 text-sm">Modes de paiement acceptés</p>
                    </div>
                    <ChevronDown className={`w-6 h-6 transition-transform ${expandedSection === 'payment' ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedSection === 'payment' && (
                    <div className="p-6 space-y-4 border-t-2 border-[#F5A623]/50">
                      <div className="space-y-3">
                        <label className="flex items-center gap-3 cursor-pointer p-3 hover:bg-white/5 rounded-lg transition-all">
                          <input type="checkbox" checked={acceptsCard} onChange={e => setAcceptsCard(e.target.checked)} className="w-6 h-6 rounded cursor-pointer" />
                          <span className="text-white font-semibold">💳 Cartes bancaires</span>
                        </label>
                        <label className="flex items-center gap-3 cursor-pointer p-3 hover:bg-white/5 rounded-lg transition-all">
                          <input type="checkbox" checked={acceptsBankTransfer} onChange={e => setAcceptsBankTransfer(e.target.checked)} className="w-6 h-6 rounded cursor-pointer" />
                          <span className="text-white font-semibold">🏦 Virements bancaires</span>
                        </label>
                        <label className="flex items-center gap-3 cursor-pointer p-3 hover:bg-white/5 rounded-lg transition-all">
                          <input type="checkbox" checked={acceptsCash} onChange={e => setAcceptsCash(e.target.checked)} className="w-6 h-6 rounded cursor-pointer" />
                          <span className="text-white font-semibold">💰 Paiement à la livraison</span>
                        </label>
                      </div>
                      {acceptsBankTransfer && (
                        <>
                          <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Banque</label>
                            <Input value={bankName} onChange={e => setBankName(e.target.value)} placeholder="Nom de la banque" className="h-12 rounded-xl border-2 border-[#F5A623]/50 bg-white/10 text-white placeholder-white/50" /></div>
                          <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Compte bancaire</label>
                            <Input value={bankAccount} onChange={e => setBankAccount(e.target.value)} placeholder="IBAN / RIB" className="h-12 rounded-xl border-2 border-[#F5A623]/50 bg-white/10 text-white placeholder-white/50" /></div>
                        </>
                      )}
                    </div>
                  )}
                </div>

                {/* SECTION: Réseaux Sociaux */}
                <div className="bg-gradient-to-br from-[#7ED321]/10 to-[#0077FF]/10 border-2 border-[#7ED321]/50 rounded-2xl overflow-hidden hover:shadow-2xl transition-all">
                  <button
                    type="button"
                    onClick={() => setExpandedSection(expandedSection === 'social' ? null : 'social')}
                    className="w-full flex items-center gap-4 p-6 bg-gradient-to-r from-[#7ED321]/20 to-[#0077FF]/20 hover:from-[#7ED321]/30 hover:to-[#0077FF]/30 transition-all"
                  >
                    <div className="text-3xl">🌐</div>
                    <div className="text-left flex-1">
                      <span className="font-bold text-lg">Réseaux sociaux & Contact</span>
                      <p className="text-white/60 text-sm">Connectez vos profils</p>
                    </div>
                    <ChevronDown className={`w-6 h-6 transition-transform ${expandedSection === 'social' ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedSection === 'social' && (
                    <div className="p-6 space-y-4 border-t-2 border-[#7ED321]/50">
                      <div className="grid md:grid-cols-2 gap-4">
                        <div><Input value={instagram} onChange={e => setInstagram(e.target.value)} placeholder="📸 Instagram @..." className="h-12 rounded-xl border-2 border-[#7ED321]/50 bg-white/10 text-white placeholder-white/50" /></div>
                        <div><Input value={facebook} onChange={e => setFacebook(e.target.value)} placeholder="f Facebook" className="h-12 rounded-xl border-2 border-[#7ED321]/50 bg-white/10 text-white placeholder-white/50" /></div>
                        <div><Input value={whatsapp} onChange={e => setWhatsapp(e.target.value)} placeholder="💬 WhatsApp +213..." className="h-12 rounded-xl border-2 border-[#7ED321]/50 bg-white/10 text-white placeholder-white/50" /></div>
                        <div><Input value={website} onChange={e => setWebsite(e.target.value)} placeholder="🌍 Site web https://..." className="h-12 rounded-xl border-2 border-[#7ED321]/50 bg-white/10 text-white placeholder-white/50" /></div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Submit Button */}
                <div className="flex gap-4 justify-center pt-4">
                  <Button type="submit" disabled={creating} className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white rounded-xl px-12 py-4 font-bold text-lg shadow-2xl hover:shadow-3xl transition-all hover:scale-105">
                    {creating ? '⏳ Création en cours...' : '🚀 Créer ma boutique complète'}
                  </Button>
                  <Link to="/dashboard" className="bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white rounded-xl px-8 py-4 font-bold transition-all hover:shadow-lg">
                    ← Retour
                  </Link>
                </div>
              </form>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
