import { useState } from "react";
import { Header } from "../components/Header";
import { Footer } from "../components/Footer";
import { Search, Filter } from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Card, CardContent } from "../components/ui/card";
import { ImageWithFallback } from "../components/figma/ImageWithFallback";
import { useNavigate } from "react-router-dom";

const categories = ["Tous", "Mode", "High-tech", "Beauté", "Alimentation", "Sport", "Déco", "Services", "Livres", "Santé"];

const templates = [
  // Mode & Fashion
  {
    id: 1,
    title: "Fashion Store",
    category: "Mode",
    image: "https://images.unsplash.com/photo-1761090617068-f1b3257d27ad?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmYXNoaW9uJTIwYm91dGlxdWUlMjBzdG9yZXxlbnwxfHx8fDE3NjQ1NjY4NjR8MA&ixlib=rb-4.1.0&q=80&w=1080",
    description: "Template élégant pour boutique de mode avec galerie produits",
    features: ["Galerie de mode", "Panier achats", "Paiement sécurisé"],
  },
  {
    id: 2,
    title: "Urban Style",
    category: "Mode",
    image: "https://images.unsplash.com/photo-1745716154e27b97f8c73b39a9ef3de5a09efd08?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Style urbain et contemporain pour vêtements tendance",
    features: ["Design moderne", "Filtres produits", "Avis clients"],
  },
  {
    id: 3,
    title: "Luxury Couture",
    category: "Mode",
    image: "https://images.unsplash.com/photo-1770566174775-f37a92f3370f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Template premium pour haute couture et luxe",
    features: ["Design raffiné", "Showroom virtuel", "Collections VIP"],
  },
  
  // High-Tech
  {
    id: 4,
    title: "Tech Shop",
    category: "High-tech",
    image: "https://images.unsplash.com/photo-1761207850745-d41a776ef897?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwZ2FkZ2V0cyUyMHNob3B8ZW58MXx8fHwxNzY0NjEyMDY4fDA&ixlib=rb-4.1.0&q=80&w=1080",
    description: "Design moderne pour produits technologiques",
    features: ["Spécifications détaillées", "Comparaison produits", "Support technique"],
  },
  {
    id: 5,
    title: "Gadget Pro",
    category: "High-tech",
    image: "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Pour les dernières innovations et gadgets",
    features: ["Critiques produits", "Notifications de stock", "Programme fidélité"],
  },
  {
    id: 6,
    title: "Electronics Hub",
    category: "High-tech",
    image: "https://images.unsplash.com/photo-1505228395891-9a51e7e86e81?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Centre complet pour appareils électroniques",
    features: ["Blog technologie", "Conseils d'experts", "Garantie étendue"],
  },
  
  // Beauté & Cosmétiques
  {
    id: 7,
    title: "Beauty Haven",
    category: "Beauté",
    image: "https://images.unsplash.com/photo-1624574966266-1cdd65b74500?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxiZWF1dHklMjBjb3NtZXRpY3MlMjBwcm9kdWN0c3xlbnwxfHx8fDE3NjQ1NzI3OTd8MA&ixlib=rb-4.1.0&q=80&w=1080",
    description: "Template raffiné pour cosmétiques et soins",
    features: ["Guides beauté", "Consultations", "Programmes fidélité"],
  },
  {
    id: 8,
    title: "Glow Beauty",
    category: "Beauté",
    image: "https://images.unsplash.com/photo-1576426394840-c51e7f1dc5d8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Soins et beauté haut de gamme",
    features: ["Recommandations IA", "Test produits", "Tutoriels vidéo"],
  },
  {
    id: 9,
    title: "Skincare Studio",
    category: "Beauté",
    image: "https://images.unsplash.com/photo-1556228578-8c89e6adf883?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Spécialisé en soins naturels et bio",
    features: ["Ingrédients naturels", "Certifications", "Abonnements beauté"],
  },
  
  // Alimentation & Gastronomie
  {
    id: 10,
    title: "Gourmet Delights",
    category: "Alimentation",
    image: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Marché gourmet en ligne avec produits spécialisés",
    features: ["Recettes cuisines", "Livraison rapide", "Producteurs locaux"],
  },
  {
    id: 11,
    title: "Organic Market",
    category: "Alimentation",
    image: "https://images.unsplash.com/photo-1488459716781-6f3ee727a471?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Fruits, légumes et produits bio certifiés",
    features: ["Produits bio", "Livraison hebdomadaire", "Paniers personnalisés"],
  },
  {
    id: 12,
    title: "Café Artisan",
    category: "Alimentation",
    image: "https://images.unsplash.com/photo-1540432048c9f4a1e9e0992ac1f6b9e61e4df0cb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Vente de café et thé de qualité premium",
    features: ["Sourcing éthique", "Abonnements mensuels", "Blog café"],
  },
  
  // Sport & Fitness
  {
    id: 13,
    title: "Active Wear",
    category: "Sport",
    image: "https://images.unsplash.com/photo-1552668473-d5ddb56e7ea0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Vêtements de sport haute performance",
    features: ["Guides d'entrainement", "Suiveur de forme", "Livraison gratuite"],
  },
  {
    id: 14,
    title: "Fitness Hub",
    category: "Sport",
    image: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Équipements de fitness et accessoires",
    features: ["Plans d'entrainement", "Consultation gratuite", "Garantie 2 ans"],
  },
  {
    id: 15,
    title: "Sports Equipment",
    category: "Sport",
    image: "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Équipements sportifs pour tous les sports",
    features: ["Avis experts", "Vidéos tutoriels", "Retours gratuits"],
  },
  
  // Décoration & Maison
  {
    id: 16,
    title: "Home Décor",
    category: "Déco",
    image: "https://images.unsplash.com/photo-1578500494198-246f612d03b3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Mobilier et décoration pour votre intérieur",
    features: ["Visualiseur 3D", "Conseil décoration", "Service livraison"],
  },
  {
    id: 17,
    title: "Modern Living",
    category: "Déco",
    image: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Design contemporain et minimaliste",
    features: ["Inspiration design", "Configuration pièces", "Crédits paiement"],
  },
  {
    id: 18,
    title: "Rustic Home",
    category: "Déco",
    image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Décoration rustique et vintage",
    features: ["Sélection curatée", "Livraison assurée", "Satisfaction garantie"],
  },
  
  // Services
  {
    id: 19,
    title: "Service Professionnel",
    category: "Services",
    image: "https://images.unsplash.com/photo-1552664730-d307ca884978?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Template pour services professionnels B2B",
    features: ["Réservation en ligne", "Devis automatisés", "Calendrier intégré"],
  },
  {
    id: 20,
    title: "Salon & Spa",
    category: "Services",
    image: "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Gestion complète salon de beauté et spa",
    features: ["Réservation clients", "Gestion équipe", "Promotions saisonnières"],
  },
  
  // Livres & Éducation
  {
    id: 21,
    title: "Digital Library",
    category: "Livres",
    image: "https://images.unsplash.com/photo-1507842217343-583f7270bfba?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Librairie numérique avec ebooks et audiobooks",
    features: ["Lecteur intégré", "Bibliothèque personnelle", "Partage social"],
  },
  {
    id: 22,
    title: "Book Store",
    category: "Livres",
    image: "https://images.unsplash.com/photo-1507842307343-583f90315ef3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Librairie en ligne avec livres physiques",
    features: ["Recommandations IA", "Critiques lecteurs", "Précommandes"],
  },
  
  // Santé & Bien-être
  {
    id: 23,
    title: "Health Store",
    category: "Santé",
    image: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Suppléments et produits de santé naturels",
    features: ["Conseils nutritionnels", "Articles santé", "Consultation experts"],
  },
  {
    id: 24,
    title: "Wellness Hub",
    category: "Santé",
    image: "https://images.unsplash.com/photo-1506157786151-b8491531f063?crop=entropy&cs=tinysrgb&fit=max&fm=jpg",
    description: "Bien-être holistique et médecines douces",
    features: ["Cours en ligne", "Coaching personnalisé", "Programme détox"],
  },
];

export function TemplatesPage() {
  const [selectedCategory, setSelectedCategory] = useState("Tous");
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const filteredTemplates = templates.filter(template => {
    const matchesCategory = selectedCategory === "Tous" || template.category === selectedCategory;
    const matchesSearch = template.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-white dark:bg-gray-950">
      <Header />
      
      <section className="py-24 bg-gradient-to-br from-[#0077FF]/5 via-[#5AC8FA]/5 to-white">
        <div className="container mx-auto px-6">
          {/* Header */}
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h1 className="text-[#0A1A2F] mb-4" style={{ fontSize: '56px', fontWeight: '800' }}>
              Nos Templates
            </h1>
            <p className="text-[#0A1A2F]/70 text-xl">
              Découvrez notre collection de designs professionnels prêts à l'emploi
            </p>
          </div>

          {/* Search and Filter */}
          <div className="flex flex-col md:flex-row gap-4 mb-12 max-w-4xl mx-auto">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[#0A1A2F]/40" />
              <Input
                type="search"
                placeholder="Rechercher un template..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-12 h-14 rounded-xl border-2 border-gray-200 focus:border-[#0077FF]"
              />
            </div>
            <Button variant="outline" className="h-14 px-6 rounded-xl border-2 border-gray-200 hover:border-[#0077FF]">
              <Filter className="w-5 h-5 mr-2" />
              Filtres
            </Button>
          </div>

          {/* Categories */}
          <div className="flex flex-wrap gap-3 justify-center mb-12">
            {categories.map((category, index) => (
              <button
                key={index}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-3 rounded-xl transition-all ${
                  selectedCategory === category
                    ? "bg-gradient-to-r from-[#0077FF] to-[#5AC8FA] text-white shadow-lg"
                    : "bg-white border-2 border-gray-200 text-[#0A1A2F] hover:border-[#0077FF]"
                }`}
                style={{ fontWeight: selectedCategory === category ? '600' : '500' }}
              >
                {category}
              </button>
            ))}
          </div>

          {/* Templates Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredTemplates.map((template) => (
              <Card 
                key={template.id}
                className="group overflow-hidden border-2 border-gray-100 hover:border-[#0077FF]/30 hover:shadow-2xl transition-all duration-300 rounded-2xl cursor-pointer"
                onClick={() => navigate(`/templates/${template.id}`)}
              >
                <CardContent className="p-0">
                  <div className="relative overflow-hidden aspect-[4/3]">
                    <ImageWithFallback
                      src={template.image}
                      alt={template.title}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-[#0A1A2F]/80 via-[#0A1A2F]/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <Button className="bg-white text-[#0077FF] hover:bg-white/90 rounded-xl px-6">
                        Voir le template
                      </Button>
                    </div>
                  </div>
                  <div className="p-6">
                    <span className="inline-block px-3 py-1 bg-[#0077FF]/10 text-[#0077FF] text-sm rounded-full mb-3">
                      {template.category}
                    </span>
                    <h3 className="text-[#0A1A2F] mb-2" style={{ fontSize: '20px', fontWeight: '700' }}>
                      {template.title}
                    </h3>
                    <p className="text-[#0A1A2F]/70 mb-4 text-sm">
                      {template.description}
                    </p>
                    {template.features && (
                      <div className="flex flex-wrap gap-2">
                        {template.features.map((feature, idx) => (
                          <span key={idx} className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded-lg">
                            {feature}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* CTA */}
          <div className="text-center mt-16">
            <div className="inline-flex flex-col items-center gap-4 p-8 bg-gradient-to-br from-[#0077FF]/5 to-[#5AC8FA]/5 rounded-2xl border border-[#0077FF]/20">
              <p className="text-[#0A1A2F] text-xl" style={{ fontWeight: '700' }}>
                Vous ne trouvez pas ce que vous cherchez ?
              </p>
              <p className="text-[#0A1A2F]/70">
                Contactez-nous pour un template personnalisé
              </p>
              <Button 
                onClick={() => navigate("/support")}
                className="bg-[#0077FF] hover:bg-[#0077FF]/90 text-white rounded-xl px-8 h-12"
              >
                Demander un template sur mesure
              </Button>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}