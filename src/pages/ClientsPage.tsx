import { useEffect, useState } from "react";
import { DashboardHeader } from "../components/DashboardHeader";
import { DashboardSidebar } from "../components/DashboardSidebar";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { useAPI } from "../hooks/useAPI";
import { Users, Loader2, Mail, Phone, MapPin } from "lucide-react";

interface Client {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone_number?: string;
  address?: string;
  orders_count: number;
  total_spent: number;
  date_joined: string;
}

export function ClientsPage() {
  const api = useAPI();
  const [loading, setLoading] = useState(true);
  const [clients, setClients] = useState<Client[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    let ignore = false;
    async function load() {
      try {
        setLoading(true);
        setError(null);
        const res = await api.get('/users/api/clients/');
        if (!ignore) {
          if (res.ok) {
            const data = await res.json();
            setClients(data);
          } else {
            setError("Impossible de charger les clients");
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

  const filteredClients = clients.filter(client =>
    `${client.first_name} ${client.last_name}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <DashboardHeader />
      <div className="flex">
        <DashboardSidebar />
        <main className="flex-1 p-8 dark:bg-gray-950">
          <div className="mb-8">
            <h1 className="text-[#0A1A2F] dark:text-white mb-2" style={{ fontSize: "36px", fontWeight: "800" }}>
              Gérer les clients 👥
            </h1>
            <p className="text-[#0A1A2F]/60 dark:text-gray-400">Liste complète de vos clients et leurs commandes</p>
          </div>

          {/* Search Bar */}
          <Card className="mb-6 border-2 border-gray-100 dark:border-gray-800 rounded-2xl">
            <CardContent className="p-6">
              <input
                type="text"
                placeholder="Chercher par nom ou email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border-2 border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-[#0A1A2F] dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:border-[#0077FF]"
              />
            </CardContent>
          </Card>

          {loading && (
            <div className="flex items-center justify-center py-24">
              <div className="text-center">
                <Loader2 className="w-12 h-12 animate-spin text-[#0077FF] mx-auto mb-4" />
                <p className="text-[#0A1A2F]/60 dark:text-gray-400">Chargement des clients...</p>
              </div>
            </div>
          )}

          {error && (
            <Card className="border-2 border-red-200 dark:border-red-800 rounded-2xl bg-red-50 dark:bg-red-900/20">
              <CardContent className="p-6">
                <p className="text-red-700 dark:text-red-400 font-semibold">⚠️ Erreur:</p>
                <p className="text-red-600 dark:text-red-300">{error}</p>
              </CardContent>
            </Card>
          )}

          {!loading && filteredClients.length === 0 && !error && (
            <Card className="border-2 border-gray-100 dark:border-gray-800 rounded-2xl">
              <CardContent className="p-12 text-center">
                <Users className="w-16 h-16 text-gray-300 dark:text-gray-700 mx-auto mb-4" />
                <p className="text-[#0A1A2F]/60 dark:text-gray-400">Aucun client trouvé</p>
              </CardContent>
            </Card>
          )}

          {!loading && filteredClients.length > 0 && (
            <div className="grid gap-4">
              {filteredClients.map((client) => (
                <Card key={client.id} className="border-2 border-gray-100 dark:border-gray-800 rounded-2xl hover:shadow-lg transition-all">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-3">
                          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#0077FF] to-[#5AC8FA] flex items-center justify-center text-white font-bold">
                            {client.first_name.charAt(0)}{client.last_name.charAt(0)}
                          </div>
                          <div>
                            <h3 className="text-[#0A1A2F] dark:text-white font-bold text-lg">
                              {client.first_name} {client.last_name}
                            </h3>
                            <p className="text-[#0A1A2F]/60 dark:text-gray-400 text-sm">
                              Depuis {new Date(client.date_joined).toLocaleDateString('fr-FR')}
                            </p>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <div className="flex items-center gap-2 text-[#0A1A2F]/70 dark:text-gray-300 text-sm">
                            <Mail className="w-4 h-4 text-[#0077FF]" />
                            {client.email}
                          </div>
                          {client.phone_number && (
                            <div className="flex items-center gap-2 text-[#0A1A2F]/70 dark:text-gray-300 text-sm">
                              <Phone className="w-4 h-4 text-[#0077FF]" />
                              {client.phone_number}
                            </div>
                          )}
                          {client.address && (
                            <div className="flex items-center gap-2 text-[#0A1A2F]/70 dark:text-gray-300 text-sm">
                              <MapPin className="w-4 h-4 text-[#0077FF]" />
                              {client.address}
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="text-right">
                        <div className="mb-4">
                          <p className="text-2xl font-bold text-[#0A1A2F] dark:text-white">
                            {client.orders_count}
                          </p>
                          <p className="text-[#0A1A2F]/60 dark:text-gray-400 text-xs">Commandes</p>
                        </div>
                        <div>
                          <p className="text-lg font-bold text-green-600">
                            {client.total_spent.toFixed(2)} DZD
                          </p>
                          <p className="text-[#0A1A2F]/60 dark:text-gray-400 text-xs">Total dépensé</p>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
