import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import { useAPI } from "../hooks/useAPI";
import { ChevronDown, Store, Save, ArrowLeft, Mail, Phone, MapPin, CreditCard, Palette, Globe, Zap } from "lucide-react";

export function ShopSettingsPage() {
  const { user } = useAuth();
  const api = useAPI();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [shop, setShop] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expandedSection, setExpandedSection] = useState<string | null>("general");

  // State for all shop settings
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
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

  // Load shop data
  useEffect(() => {
    let ignore = false;

    async function load() {
      console.log('🔄 Loading shop settings...');
      setLoading(true);
      setError(null);
      try {
        const res = await api.get('/shop/api/my-shop/');
        if (!ignore) {
          if (res.ok) {
            const data = await res.json();
            console.log('✅ Shop loaded:', data);
            setShop(data);
            // Populate all fields
            setName(data.name || "");
            setDescription(data.description || "");
            setEmail(data.email || "");
            setPhone(data.phone || "");
            setLogo(data.logo || "");
            setBannerImage(data.bannerImage || "");
            setPrimaryColor(data.primaryColor || "#0077FF");
            setSecondaryColor(data.secondaryColor || "#5AC8FA");
            setAddress(data.address || "");
            setCity(data.city || "");
            setPostalCode(data.postalCode || "");
            setCountry(data.country || "Algérie");
            setShippingCost(data.shippingCost?.toString() || "0");
            setFreeShippingThreshold(data.freeShippingThreshold?.toString() || "1000");
            setAcceptsCard(data.acceptsCard ?? true);
            setAcceptsBankTransfer(data.acceptsBankTransfer ?? true);
            setAcceptsCash(data.acceptsCash ?? true);
            setBankName(data.bankName || "");
            setBankAccount(data.bankAccount || "");
            setMetaDescription(data.metaDescription || "");
            setMetaKeywords(data.metaKeywords || "");
            setInstagram(data.instagram || "");
            setFacebook(data.facebook || "");
            setWhatsapp(data.whatsapp || "");
            setWebsite(data.website || "");
            setCurrency(data.currency || "DZD");
            setTimezone(data.timezone || "Africa/Algiers");
            setReturnsPolicy(data.returnsPolicy || "");
            setTermsAndConditions(data.termsAndConditions || "");
          } else if (res.status === 404) {
            setError("Aucune boutique trouvée. Créez une boutique d'abord.");
          } else {
            setError("Erreur lors du chargement des paramètres");
          }
        }
      } catch (e: any) {
        if (!ignore) {
          console.error('❌ Exception:', e);
          setError(e?.message || "Erreur réseau");
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    load();
    return () => { ignore = true; };
  }, []);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    if (!shop) return;
    setSaving(true);
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
        setShop(data);
        toast.success('Paramètres sauvegardés avec succès! ✨');
      } else {
        const data = await res.json().catch(() => ({}));
        const msg = data?.detail || 'Erreur lors de la sauvegarde';
        toast.error(msg);
      }
    } catch (e: any) {
      console.error('❌ Exception:', e);
      toast.error(e?.message || 'Erreur réseau');
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#0A1A2F] via-[#0D2847] to-[#1a3a52] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="relative w-16 h-16">
            <div className="absolute inset-0 bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] rounded-full animate-spin"></div>
            <div className="absolute inset-2 bg-[#0A1A2F] rounded-full"></div>
          </div>
          <p className="text-white text-lg">Chargement des paramètres...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#0A1A2F] via-[#0D2847] to-[#1a3a52] p-8">
        <div className="max-w-4xl mx-auto">
          <Link to="/my-shop" className="inline-flex items-center gap-2 text-[#5AC8FA] hover:text-white mb-8">
            <ArrowLeft className="w-5 h-5" />
            Retour
          </Link>
          <div className="p-8 bg-red-500/20 border-2 border-red-500/50 rounded-2xl">
            <p className="text-red-300 font-bold text-lg mb-2">⚠️ Erreur</p>
            <p className="text-red-200">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0A1A2F] via-[#0D2847] to-[#1a3a52] text-white">
      {/* Header */}
      <header className="bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] shadow-2xl border-b-4 border-[#00D4FF]">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-white/20 rounded-xl backdrop-blur">
              <Store className="w-8 h-8" />
            </div>
            <div>
              <h1 className="text-4xl font-black">Paramètres de la boutique</h1>
              <p className="text-white/80 text-sm">{shop?.name || "Ma boutique"}</p>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto p-8 space-y-8">
        {/* Back button */}
        <Link to="/my-shop" className="inline-flex items-center gap-2 text-[#5AC8FA] hover:text-white transition-colors">
          <ArrowLeft className="w-5 h-5" />
          Retour à ma boutique
        </Link>

        <form onSubmit={handleSave} className="space-y-6">
          {/* SECTION: Infos Générales */}
          <div className="bg-gradient-to-br from-[#0077FF]/10 to-[#5AC8FA]/10 border-2 border-[#0077FF]/50 rounded-2xl overflow-hidden hover:shadow-2xl transition-all">
            <button
              type="button"
              onClick={() => setExpandedSection(expandedSection === 'general' ? null : 'general')}
              className="w-full flex items-center gap-4 p-6 bg-gradient-to-r from-[#0077FF]/20 to-[#5AC8FA]/20 hover:from-[#0077FF]/30 hover:to-[#5AC8FA]/30 transition-all"
            >
              <Mail className="w-6 h-6 text-[#5AC8FA]" />
              <div className="text-left flex-1">
                <span className="font-bold text-lg">Informations générales</span>
                <p className="text-white/60 text-sm">Nom, description, contact</p>
              </div>
              <ChevronDown className={`w-6 h-6 transition-transform ${expandedSection === 'general' ? 'rotate-180' : ''}`} />
            </button>
            {expandedSection === 'general' && (
              <div className="p-6 space-y-4 border-t-2 border-[#0077FF]/50">
                <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Nom</label>
                  <Input value={name} onChange={e => setName(e.target.value)} className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white" /></div>
                <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Description</label>
                  <Textarea value={description} onChange={e => setDescription(e.target.value)} rows={4} className="rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white" /></div>
                <div className="grid md:grid-cols-2 gap-4">
                  <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Email</label>
                    <Input type="email" value={email} onChange={e => setEmail(e.target.value)} className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white" /></div>
                  <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Téléphone</label>
                    <Input value={phone} onChange={e => setPhone(e.target.value)} className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white" /></div>
                </div>
                <div className="grid md:grid-cols-2 gap-4">
                  <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Devise</label>
                    <select value={currency} onChange={e => setCurrency(e.target.value)} className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white px-4">
                      <option className="bg-[#0A1A2F]">DZD</option>
                      <option className="bg-[#0A1A2F]">USD</option>
                      <option className="bg-[#0A1A2F]">EUR</option>
                    </select></div>
                  <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Fuseau horaire</label>
                    <select value={timezone} onChange={e => setTimezone(e.target.value)} className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white px-4">
                      <option className="bg-[#0A1A2F]">Africa/Algiers</option>
                      <option className="bg-[#0A1A2F]">Europe/Paris</option>
                      <option className="bg-[#0A1A2F]">UTC</option>
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
              <Palette className="w-6 h-6 text-[#5AC8FA]" />
              <div className="text-left flex-1">
                <span className="font-bold text-lg">Branding & Design</span>
                <p className="text-white/60 text-sm">Logo, couleurs, bannière</p>
              </div>
              <ChevronDown className={`w-6 h-6 transition-transform ${expandedSection === 'branding' ? 'rotate-180' : ''}`} />
            </button>
            {expandedSection === 'branding' && (
              <div className="p-6 space-y-4 border-t-2 border-[#5AC8FA]/50">
                <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">URL du logo</label>
                  <Input value={logo} onChange={e => setLogo(e.target.value)} placeholder="https://..." className="h-12 rounded-xl border-2 border-[#5AC8FA]/50 bg-white/10 text-white" /></div>
                <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">URL de la bannière</label>
                  <Input value={bannerImage} onChange={e => setBannerImage(e.target.value)} placeholder="https://..." className="h-12 rounded-xl border-2 border-[#5AC8FA]/50 bg-white/10 text-white" /></div>
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

          {/* SECTION: Adresse & Livraison */}
          <div className="bg-gradient-to-br from-[#50E3C2]/10 to-[#F5A623]/10 border-2 border-[#50E3C2]/50 rounded-2xl overflow-hidden hover:shadow-2xl transition-all">
            <button
              type="button"
              onClick={() => setExpandedSection(expandedSection === 'shipping' ? null : 'shipping')}
              className="w-full flex items-center gap-4 p-6 bg-gradient-to-r from-[#50E3C2]/20 to-[#F5A623]/20 hover:from-[#50E3C2]/30 hover:to-[#F5A623]/30 transition-all"
            >
              <MapPin className="w-6 h-6 text-[#50E3C2]" />
              <div className="text-left flex-1">
                <span className="font-bold text-lg">Adresse & Livraison</span>
                <p className="text-white/60 text-sm">Lieu, tarifs de livraison</p>
              </div>
              <ChevronDown className={`w-6 h-6 transition-transform ${expandedSection === 'shipping' ? 'rotate-180' : ''}`} />
            </button>
            {expandedSection === 'shipping' && (
              <div className="p-6 space-y-4 border-t-2 border-[#50E3C2]/50">
                <div><Input value={address} onChange={e => setAddress(e.target.value)} placeholder="Adresse" className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white" /></div>
                <div className="grid md:grid-cols-3 gap-4">
                  <div><Input value={city} onChange={e => setCity(e.target.value)} placeholder="Ville" className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white" /></div>
                  <div><Input value={postalCode} onChange={e => setPostalCode(e.target.value)} placeholder="Code postal" className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white" /></div>
                  <div><select value={country} onChange={e => setCountry(e.target.value)} className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white px-4">
                    <option className="bg-[#0A1A2F]">Algérie</option>
                    <option className="bg-[#0A1A2F]">France</option>
                    <option className="bg-[#0A1A2F]">Tunisie</option>
                  </select></div>
                </div>
                <div className="grid md:grid-cols-2 gap-4">
                  <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Coût livraison (DZD)</label>
                    <Input type="number" value={shippingCost} onChange={e => setShippingCost(e.target.value)} className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white" /></div>
                  <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Gratuit à partir de (DZD)</label>
                    <Input type="number" value={freeShippingThreshold} onChange={e => setFreeShippingThreshold(e.target.value)} className="h-12 rounded-xl border-2 border-[#50E3C2]/50 bg-white/10 text-white" /></div>
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
              <CreditCard className="w-6 h-6 text-[#F5A623]" />
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
                    <div><Input value={bankName} onChange={e => setBankName(e.target.value)} placeholder="Nom de la banque" className="h-12 rounded-xl border-2 border-[#F5A623]/50 bg-white/10 text-white" /></div>
                    <div><Input value={bankAccount} onChange={e => setBankAccount(e.target.value)} placeholder="IBAN / RIB" className="h-12 rounded-xl border-2 border-[#F5A623]/50 bg-white/10 text-white" /></div>
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
              <Globe className="w-6 h-6 text-[#7ED321]" />
              <div className="text-left flex-1">
                <span className="font-bold text-lg">Réseaux sociaux</span>
                <p className="text-white/60 text-sm">Connectez vos profils</p>
              </div>
              <ChevronDown className={`w-6 h-6 transition-transform ${expandedSection === 'social' ? 'rotate-180' : ''}`} />
            </button>
            {expandedSection === 'social' && (
              <div className="p-6 space-y-4 border-t-2 border-[#7ED321]/50">
                <div className="grid md:grid-cols-2 gap-4">
                  <Input value={instagram} onChange={e => setInstagram(e.target.value)} placeholder="📸 Instagram @..." className="h-12 rounded-xl border-2 border-[#7ED321]/50 bg-white/10 text-white" />
                  <Input value={facebook} onChange={e => setFacebook(e.target.value)} placeholder="f Facebook" className="h-12 rounded-xl border-2 border-[#7ED321]/50 bg-white/10 text-white" />
                  <Input value={whatsapp} onChange={e => setWhatsapp(e.target.value)} placeholder="💬 WhatsApp +213..." className="h-12 rounded-xl border-2 border-[#7ED321]/50 bg-white/10 text-white" />
                  <Input value={website} onChange={e => setWebsite(e.target.value)} placeholder="🌍 Site web https://..." className="h-12 rounded-xl border-2 border-[#7ED321]/50 bg-white/10 text-white" />
                </div>
              </div>
            )}
          </div>

          {/* SECTION: SEO & Politiques */}
          <div className="bg-gradient-to-br from-[#0077FF]/10 to-[#5AC8FA]/10 border-2 border-[#0077FF]/50 rounded-2xl overflow-hidden hover:shadow-2xl transition-all">
            <button
              type="button"
              onClick={() => setExpandedSection(expandedSection === 'seo' ? null : 'seo')}
              className="w-full flex items-center gap-4 p-6 bg-gradient-to-r from-[#0077FF]/20 to-[#5AC8FA]/20 hover:from-[#0077FF]/30 hover:to-[#5AC8FA]/30 transition-all"
            >
              <Zap className="w-6 h-6 text-[#0077FF]" />
              <div className="text-left flex-1">
                <span className="font-bold text-lg">SEO & Politiques</span>
                <p className="text-white/60 text-sm">Optimisation et conditions</p>
              </div>
              <ChevronDown className={`w-6 h-6 transition-transform ${expandedSection === 'seo' ? 'rotate-180' : ''}`} />
            </button>
            {expandedSection === 'seo' && (
              <div className="p-6 space-y-4 border-t-2 border-[#0077FF]/50">
                <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Métadescription (SEO)</label>
                  <Textarea value={metaDescription} onChange={e => setMetaDescription(e.target.value)} rows={2} className="rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white" /></div>
                <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Mots-clés (SEO)</label>
                  <Input value={metaKeywords} onChange={e => setMetaKeywords(e.target.value)} placeholder="mot1, mot2, mot3" className="h-12 rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white" /></div>
                <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Politique de retour</label>
                  <Textarea value={returnsPolicy} onChange={e => setReturnsPolicy(e.target.value)} rows={3} className="rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white" /></div>
                <div><label className="text-sm font-bold text-[#5AC8FA] block mb-2">Conditions d'utilisation</label>
                  <Textarea value={termsAndConditions} onChange={e => setTermsAndConditions(e.target.value)} rows={3} className="rounded-xl border-2 border-[#0077FF]/50 bg-white/10 text-white" /></div>
              </div>
            )}
          </div>

          {/* Save Button */}
          <div className="flex gap-4 justify-center pt-4">
            <Button type="submit" disabled={saving} className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white rounded-xl px-12 py-4 font-bold text-lg shadow-2xl hover:shadow-3xl transition-all hover:scale-105 flex items-center gap-2">
              <Save className="w-5 h-5" />
              {saving ? 'Sauvegarde en cours...' : 'Enregistrer les modifications'}
            </Button>
            <Link to="/my-shop" className="bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white rounded-xl px-8 py-4 font-bold transition-all hover:shadow-lg flex items-center gap-2">
              <ArrowLeft className="w-5 h-5" />
              Retour
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
