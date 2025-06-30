import tkinter as tk
from tkinter import messagebox
import pandas as pd
import customtkinter as ctk
from PIL import Image, ImageDraw
import webbrowser
import json
import os


# Modern tema ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

USER_DATA_FILE = "users.json"
USER_LISTS_FILE = "user_lists.json"

# Renk paleti
COLORS = {
    'primary': '#1f538d',
    'secondary': '#14375e',
    'accent': '#ffd700',
    'background': '#0f1419',
    'surface': '#1a1f24',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0b0',
    'success': '#4ade80',
    'error': '#ef4444',
    'warning': '#f59e0b'
}


class ModernMovieApp:
    def __init__(self):
        self.current_user = None
        self.df = None
        self.current_movies_df = None  # Bu satırı ekleyin - gösterilen filmleri takip eder
        self.load_data()
        self.user_lists = {
            'liked': [],
            'disliked': [],
            'watched': [],
            'to_watch': [],
            'favorites': []
        }

    def load_data(self):
        """CSV dosyasını yükle ve işle"""
        try:
            file_path = r"C:\Users\sarme\Desktop\edu\3\seminer 1\Top_10000_Movies_IMDb.csv"  # Dosya yolunu güncelleyin
            self.df = pd.read_csv(file_path)
            self.df.rename(columns={
                "Movie Name": "title",
                "Directors": "director",
                "Stars": "actors",
                "Genre": "genre",
                "Plot": "plot",
                "Rating": "rating",
                "Runtime": "runtime",
                "Metascore": "metascore",
                "Votes": "votes",
                "Gross": "gross",
                "Link": "link"
            }, inplace=True)
        except FileNotFoundError:
            messagebox.showerror("Hata", "Film veritabanı dosyası bulunamadı!")


    def create_modern_button(self, parent, text, command, color=None, hover_color=None):
        """Modern stil buton oluştur"""
        btn_color = color or COLORS['primary']
        btn_hover = hover_color or COLORS['secondary']

        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=btn_color,
            hover_color=btn_hover,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        return button

    def create_movie_card(self, parent, movie_data):
        """Film kartı oluştur"""
        card_frame = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['secondary']
        )

        # Film başlığı
        title_label = ctk.CTkLabel(
            card_frame,
            text=movie_data['title'][:40] + ("..." if len(movie_data['title']) > 40 else ""),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(15, 5), padx=15, anchor="w")

        # Film bilgileri
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=5)

        # Rating ve genre
        rating_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        rating_frame.pack(fill="x")

        rating_label = ctk.CTkLabel(
            rating_frame,
            text=f"⭐ {movie_data['rating']}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['accent']
        )
        rating_label.pack(side="left")

        genre_label = ctk.CTkLabel(
            rating_frame,
            text=f"{movie_data['genre'][:20]}...",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_secondary']
        )
        genre_label.pack(side="right")

        # Butonlar
        button_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(10, 15))

        details_btn = ctk.CTkButton(
            button_frame,
            text="Detaylar",
            command=lambda: self.show_movie_details(movie_data['title']),
            width=80,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        details_btn.pack(side="left", padx=(0, 5))

        add_btn = ctk.CTkButton(
            button_frame,
            text="➕",
            command=lambda: self.show_add_menu(movie_data['title']),
            width=30,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        add_btn.pack(side="right")

        return card_frame

    def show_login_window(self):
        """Modern giriş ekranı"""
        self.login_window = ctk.CTk()
        self.login_window.title("Film Tavsiye Uygulaması - Giriş")
        self.login_window.geometry("450x550")
        self.login_window.resizable(False, False)

        # Ortalama
        screen_width = self.login_window.winfo_screenwidth()
        screen_height = self.login_window.winfo_screenheight()
        x = (screen_width - 450) // 2
        y = (screen_height - 550) // 2
        self.login_window.geometry(f"450x550+{x}+{y}")

        # Ana container
        main_frame = ctk.CTkFrame(self.login_window, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Logo/Başlık
        title_label = ctk.CTkLabel(
            main_frame,
            text="🎬 CINEWHISPER",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=COLORS['accent']
        )
        title_label.pack(pady=(40, 10))

        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Kişiselleştirilmiş Film Tavsiyeleri",
            font=ctk.CTkFont(size=14),
            text_color=COLORS['text_secondary']
        )
        subtitle_label.pack(pady=(0, 30))

        # Giriş formu
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=40)

        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Kullanıcı Adı",
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.username_entry.pack(fill="x", pady=(0, 15))

        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Şifre",
            show="*",
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.password_entry.pack(fill="x", pady=(0, 25))

        # Giriş butonu
        login_btn = self.create_modern_button(
            form_frame,
            "Giriş Yap",
            self.login,
            COLORS['primary'],
            COLORS['secondary']
        )
        login_btn.pack(fill="x", pady=(0, 15))

        # Kayıt butonu
        register_btn = self.create_modern_button(
            form_frame,
            "Yeni Hesap Oluştur",
            self.show_register_window,
            COLORS['surface'],
            COLORS['secondary']
        )
        register_btn.pack(fill="x")

        # Bind Enter key
        self.login_window.bind('<Return>', lambda e: self.login())

        self.login_window.mainloop()

    def show_register_window(self):
        """Modern kayıt ekranı"""
        self.login_window.destroy()

        self.register_window = ctk.CTk()
        self.register_window.title("Yeni Hesap Oluştur")
        self.register_window.geometry("450x600")
        self.register_window.resizable(False, False)

        # Ortalama
        screen_width = self.register_window.winfo_screenwidth()
        screen_height = self.register_window.winfo_screenheight()
        x = (screen_width - 450) // 2
        y = (screen_height - 600) // 2
        self.register_window.geometry(f"450x600+{x}+{y}")

        # Ana container
        main_frame = ctk.CTkFrame(self.register_window, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Başlık
        title_label = ctk.CTkLabel(
            main_frame,
            text="Hesap Oluştur",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS['accent']
        )
        title_label.pack(pady=(30, 20))

        # Form
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=40)

        self.reg_username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Kullanıcı Adı",
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.reg_username_entry.pack(fill="x", pady=(0, 15))

        self.reg_password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Şifre",
            show="*",
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.reg_password_entry.pack(fill="x", pady=(0, 15))

        self.reg_confirm_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Şifreyi Tekrar Girin",
            show="*",
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.reg_confirm_entry.pack(fill="x", pady=(0, 25))

        # Butonlar
        register_btn = self.create_modern_button(
            form_frame,
            "Hesap Oluştur",
            self.register,
            COLORS['success']
        )
        register_btn.pack(fill="x", pady=(0, 15))

        back_btn = self.create_modern_button(
            form_frame,
            "Geri Dön",
            self.back_to_login,
            COLORS['surface']
        )
        back_btn.pack(fill="x")

        self.register_window.mainloop()

    def show_main_window(self):
        """Ana uygulama ekranı"""
        self.main_window = ctk.CTk()
        self.main_window.title("CineMatch - Film Tavsiye Uygulaması")
        self.main_window.state('zoomed')  # Tam ekran

        # Ana container
        main_container = ctk.CTkFrame(self.main_window, corner_radius=0)
        main_container.pack(fill="both", expand=True)

        # Üst bar
        top_bar = ctk.CTkFrame(main_container, height=70, corner_radius=0)
        top_bar.pack(fill="x", padx=0, pady=0)
        top_bar.pack_propagate(False)

        # Logo ve hoşgeldin mesajı
        logo_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=15)

        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🎬 CineMatch",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS['accent']
        )
        logo_label.pack(side="left")

        welcome_label = ctk.CTkLabel(
            logo_frame,
            text=f"Hoşgeldin, {self.current_user}!",
            font=ctk.CTkFont(size=14),
            text_color=COLORS['text_secondary']
        )
        welcome_label.pack(side="left", padx=(20, 0))

        # Üst butonlar
        button_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        button_frame.pack(side="right", padx=20, pady=15)

        lists_btn = ctk.CTkButton(
            button_frame,
            text="📋 Listelerim",
            command=self.show_lists,
            width=120,
            height=35
        )
        lists_btn.pack(side="right", padx=(10, 0))

        profile_btn = ctk.CTkButton(
            button_frame,
            text="👤 Profil",
            command=self.show_profile,
            width=120,
            height=35
        )
        profile_btn.pack(side="right", padx=(10, 0))

        logout_btn = ctk.CTkButton(
            button_frame,
            text="🚪 Çıkış",
            command=self.logout,
            width=120,
            height=35,
            fg_color=COLORS['error']
        )
        logout_btn.pack(side="right")

        # Ana içerik alanı
        content_frame = ctk.CTkFrame(main_container, corner_radius=0)
        content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Sol panel - Filtreler
        left_panel = ctk.CTkFrame(content_frame, width=350, corner_radius=15)
        left_panel.pack(side="left", fill="y", padx=(0, 10), pady=10)
        left_panel.pack_propagate(False)

        self.create_filter_panel(left_panel)

        # Sağ panel - Film listesi
        right_panel = ctk.CTkFrame(content_frame, corner_radius=15)
        right_panel.pack(side="right", fill="both", expand=True, pady=10)

        self.create_movie_panel(right_panel)

        self.main_window.mainloop()

    def create_filter_panel(self, parent):
        """Filtre paneli oluştur"""
        title_label = ctk.CTkLabel(
            parent,
            text="🔍 Film Filtrele",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS['accent']
        )
        title_label.pack(pady=(20, 30))

        # Filtre alanları
        filter_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20)

        # Anahtar Kelime Arama (EN ÜST)
        keyword_label = ctk.CTkLabel(filter_frame, text="Anahtar Kelime:", font=ctk.CTkFont(size=14, weight="bold"))
        keyword_label.pack(anchor="w", pady=(0, 5))

        self.keyword_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Film adı, konu veya anahtar kelime girin",
            height=40,
            corner_radius=10
        )
        self.keyword_entry.pack(fill="x", pady=(0, 20))

        # Tür
        genre_label = ctk.CTkLabel(filter_frame, text="Tür:", font=ctk.CTkFont(size=14, weight="bold"))
        genre_label.pack(anchor="w", pady=(0, 5))

        self.genre_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="örn: Action, Comedy, Drama",
            height=40,
            corner_radius=10
        )
        self.genre_entry.pack(fill="x", pady=(0, 20))

        # Yönetmen
        director_label = ctk.CTkLabel(filter_frame, text="Yönetmen:", font=ctk.CTkFont(size=14, weight="bold"))
        director_label.pack(anchor="w", pady=(0, 5))

        self.director_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="örn: Christopher Nolan",
            height=40,
            corner_radius=10
        )
        self.director_entry.pack(fill="x", pady=(0, 20))

        # Oyuncu
        actor_label = ctk.CTkLabel(filter_frame, text="Oyuncu:", font=ctk.CTkFont(size=14, weight="bold"))
        actor_label.pack(anchor="w", pady=(0, 5))

        self.actor_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="örn: Leonardo DiCaprio",
            height=40,
            corner_radius=10
        )
        self.actor_entry.pack(fill="x", pady=(0, 20))

        # Minimum puan
        rating_label = ctk.CTkLabel(filter_frame, text="Minimum IMDb Puanı:", font=ctk.CTkFont(size=14, weight="bold"))
        rating_label.pack(anchor="w", pady=(0, 5))

        self.rating_slider = ctk.CTkSlider(
            filter_frame,
            from_=0,
            to=10,
            number_of_steps=100,
            height=20
        )
        self.rating_slider.pack(fill="x", pady=(0, 10))
        self.rating_slider.set(7.0)

        self.rating_value_label = ctk.CTkLabel(
            filter_frame,
            text="7.0",
            font=ctk.CTkFont(size=12)
        )
        self.rating_value_label.pack(pady=(0, 20))

        self.rating_slider.configure(command=self.update_rating_label)

        # Arama butonu
        search_btn = self.create_modern_button(
            filter_frame,
            "🎯 Film Öner",
            self.search_movies,
            COLORS['success']
        )
        search_btn.pack(fill="x", pady=(10, 0))

        # Temizle butonu
        clear_btn = self.create_modern_button(
            filter_frame,
            "🧹 Temizle",
            self.clear_filters,
            COLORS['warning']
        )
        clear_btn.pack(fill="x", pady=(10, 20))

    def create_movie_panel(self, parent):
        """Film paneli oluştur"""
        # Başlık
        title_frame = ctk.CTkFrame(parent, fg_color="transparent", height=60)
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        title_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            title_frame,
            text="🎬 Önerilen Filmler",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS['accent']
        )
        title_label.pack(side="left", pady=15)

        # Sıralama seçenekleri
        sort_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        sort_frame.pack(side="right", pady=15)

        sort_label = ctk.CTkLabel(sort_frame, text="Sırala:", font=ctk.CTkFont(size=12))
        sort_label.pack(side="left", padx=(0, 10))

        self.sort_option = ctk.CTkOptionMenu(
            sort_frame,
            values=["Puana Göre", "Alfabetik"],
            command=self.sort_movies,
            width=120
        )
        self.sort_option.pack(side="left")

        # Scrollable film listesi
        self.movie_scroll_frame = ctk.CTkScrollableFrame(
            parent,
            corner_radius=10,
            fg_color=COLORS['background']
        )
        self.movie_scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # İlk yükleme - popüler filmler
        self.load_popular_movies()

    def load_popular_movies(self):
        """Popüler filmleri yükle"""
        if self.df is not None:
            popular_movies = self.df.nlargest(20, 'rating')
            self.current_movies_df = popular_movies  # Bu satırı ekleyin
            self.display_movies(popular_movies)
    def display_movies(self, movies_df):
        """Filmleri ekranda göster"""
        # Mevcut filmleri sakla
        self.current_movies_df = movies_df.copy()

        # Mevcut widgetları temizle
        for widget in self.movie_scroll_frame.winfo_children():
            widget.destroy()

        if movies_df.empty:
            no_results_label = ctk.CTkLabel(
                self.movie_scroll_frame,
                text="😔 Aradığınız kriterlere uygun film bulunamadı",
                font=ctk.CTkFont(size=16),
                text_color=COLORS['text_secondary']
            )
            no_results_label.pack(pady=50)
            return

        # Film kartlarını oluştur
        for _, movie in movies_df.head(50).iterrows():  # İlk 50 film
            movie_card = self.create_movie_card(self.movie_scroll_frame, movie)
            movie_card.pack(fill="x", padx=10, pady=5)

    # Yardımcı metodlar
    def update_rating_label(self, value):
        self.rating_value_label.configure(text=f"{value:.1f}")

    def clear_filters(self):
        self.keyword_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.director_entry.delete(0, tk.END)
        self.actor_entry.delete(0, tk.END)
        self.rating_slider.set(7.0)
        self.load_popular_movies()

    def search_movies(self):
        """Film arama fonksiyonu"""
        if self.df is None:
            return

        filtered_df = self.df.copy()

        # Filtreleri uygula
        keyword_filter = self.keyword_entry.get().strip()
        genre_filter = self.genre_entry.get().strip()
        director_filter = self.director_entry.get().strip()
        actor_filter = self.actor_entry.get().strip()
        min_rating = self.rating_slider.get()

        # Anahtar kelime araması - film adı, plot ve tüm sütunlarda arama
        if keyword_filter:
            keyword_mask = (
                filtered_df['title'].str.contains(keyword_filter, case=False, na=False) |
                filtered_df['plot'].str.contains(keyword_filter, case=False, na=False) |
                filtered_df['genre'].str.contains(keyword_filter, case=False, na=False) |
                filtered_df['director'].str.contains(keyword_filter, case=False, na=False) |
                filtered_df['actors'].str.contains(keyword_filter, case=False, na=False)
            )
            filtered_df = filtered_df[keyword_mask]

        if genre_filter:
            filtered_df = filtered_df[filtered_df['genre'].str.contains(genre_filter, case=False, na=False)]
        if director_filter:
            filtered_df = filtered_df[filtered_df['director'].str.contains(director_filter, case=False, na=False)]
        if actor_filter:
            filtered_df = filtered_df[filtered_df['actors'].str.contains(actor_filter, case=False, na=False)]

        filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

        self.display_movies(filtered_df.sort_values('rating', ascending=False))

    def sort_movies(self, sort_by):
        """Film sıralama"""
        if self.current_movies_df is None or self.current_movies_df.empty:
            return

        sorted_df = self.current_movies_df.copy()

        if sort_by == "Puana Göre":
            sorted_df = sorted_df.sort_values('rating', ascending=False)

        elif sort_by == "Alfabetik":
            sorted_df = sorted_df.sort_values('title', ascending=True)

        # Sıralanmış filmleri görüntüle
        self.display_movies(sorted_df)

    def show_movie_details(self, movie_title):
        """Film detay ekranı"""
        movie_data = self.df[self.df['title'] == movie_title].iloc[0]

        detail_window = ctk.CTkToplevel(self.main_window)
        detail_window.title(f"Film Detayları - {movie_title}")
        detail_window.geometry("800x600")
        detail_window.resizable(True, True)
        detail_window.lift()  # Pencereyi öne getir
        detail_window.attributes('-topmost', True)  # Her zaman en üstte
        detail_window.focus()  # Odağı pencereye ver
        detail_window.grab_set()  # Modal davranış (isteğe bağlı)
        # Detay içeriği
        main_frame = ctk.CTkScrollableFrame(detail_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        def on_closing():
            detail_window.grab_release()
            detail_window.destroy()

        detail_window.protocol("WM_DELETE_WINDOW", on_closing)
        # Film başlığı
        title_label = ctk.CTkLabel(
            main_frame,
            text=movie_data['title'],
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS['accent']
        )
        title_label.pack(pady=(0, 20))

        # Film bilgileri grid
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))

        info_data = [
            ("🎭 Tür:", movie_data['genre']),
            ("⭐ IMDb Puanı:", f"{movie_data['rating']}/10"),
            ("⏰ Süre:", movie_data['runtime']),
            ("🎬 Yönetmen:", movie_data['director']),
            ("🎭 Oyuncular:", movie_data['actors'][:100] + "..."),
        ]

        for i, (label, value) in enumerate(info_data):
            label_widget = ctk.CTkLabel(
                info_frame,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            label_widget.grid(row=i, column=0, sticky="w", padx=20, pady=10)

            value_widget = ctk.CTkLabel(
                info_frame,
                text=str(value),
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            value_widget.grid(row=i, column=1, sticky="w", padx=20, pady=10)

        # Plot
        plot_label = ctk.CTkLabel(
            main_frame,
            text="📖 Özet:",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        plot_label.pack(anchor="w", pady=(20, 10))

        plot_text = ctk.CTkTextbox(
            main_frame,
            height=150,
            font=ctk.CTkFont(size=12)
        )
        plot_text.pack(fill="x", pady=(0, 20))
        plot_text.insert("0.0", movie_data['plot'])
        plot_text.configure(state="disabled")

        # Butonlar
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)

        imdb_btn = self.create_modern_button(
            button_frame,
            "🌐 IMDb'de Görüntüle",
            lambda: webbrowser.open(movie_data['link']),
            COLORS['primary']
        )
        imdb_btn.pack(side="left", padx=(0, 10))

        add_favorite_btn = self.create_modern_button(
            button_frame,
            "⭐ Favorilere Ekle",
            lambda: self.add_to_list('favorites', movie_title),
            COLORS['accent']
        )
        add_favorite_btn.pack(side="left", padx=10)

    def show_add_menu(self, movie_title):
        """Film ekleme menüsü"""
        add_window = ctk.CTkToplevel(self.main_window)
        add_window.title("Listeye Ekle")
        add_window.lift()
        add_window.attributes('-topmost', True)
        add_window.focus()
        add_window.geometry("300x400")
        add_window.resizable(False, False)

        title_label = ctk.CTkLabel(
            add_window,
            text=f"'{movie_title[:30]}...' filmini hangi listeye eklemek istiyorsunuz?",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=250
        )
        title_label.pack(pady=20, padx=20)

        buttons = [
            ("👍 Beğendiklerim", 'liked', COLORS['success']),
            ("👎 Beğenmediklerim", 'disliked', COLORS['error']),
            ("✅ İzlediklerim", 'watched', COLORS['primary']),
            ("📝 İzleyeceklerim", 'to_watch', COLORS['warning']),
            ("⭐ Favorilerim", 'favorites', COLORS['accent'])
        ]

        for text, list_name, color in buttons:
            btn = self.create_modern_button(
                add_window,
                text,
                lambda ln=list_name: [self.add_to_list(ln, movie_title), add_window.destroy()],
                color
            )
            btn.pack(pady=5, padx=20, fill="x")

    def add_to_list(self, list_name, movie_title):
        """Film listesine ekle"""
        if movie_title not in self.user_lists[list_name]:
            self.user_lists[list_name].append(movie_title)
            self.save_user_lists()

            list_names = {
                'liked': 'Beğendiklerim',
                'disliked': 'Beğenmediklerim',
                'watched': 'İzlediklerim',
                'to_watch': 'İzleyeceklerim',
                'favorites': 'Favorilerim'
            }

            messagebox.showinfo(
                "Başarılı",
                f"'{movie_title}' filmi {list_names[list_name]} listesine eklendi!"
            )
        else:
            messagebox.showwarning("Uyarı", "Bu film zaten listede mevcut!")

    def show_lists(self):
        """Kullanıcı listelerini göster"""
        lists_window = ctk.CTkToplevel(self.main_window)
        lists_window.title("Film Listelerim")
        lists_window.lift()
        lists_window.attributes('-topmost', True)
        lists_window.focus()
        lists_window.geometry("1000x700")
        lists_window.resizable(True, True)

        def on_closing():
            lists_window.grab_release()
            lists_window.destroy()

        lists_window.protocol("WM_DELETE_WINDOW", on_closing)
        # Ana container
        main_frame = ctk.CTkFrame(lists_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Başlık
        title_label = ctk.CTkLabel(
            main_frame,
            text="📋 Film Listelerim",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS['accent']
        )
        title_label.pack(pady=(20, 30))

        # Tab view oluştur
        tabview = ctk.CTkTabview(main_frame, width=950, height=600)
        tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        list_info = [
            ("👍 Beğendiklerim", "liked", COLORS['success']),
            ("👎 Beğenmediklerim", "disliked", COLORS['error']),
            ("✅ İzlediklerim", "watched", COLORS['primary']),
            ("📝 İzleyeceklerim", "to_watch", COLORS['warning']),
            ("⭐ Favorilerim", "favorites", COLORS['accent'])
        ]

        for tab_name, list_key, color in list_info:
            tab = tabview.add(tab_name)
            self.create_list_tab(tab, list_key, color)

    def create_list_tab(self, parent, list_key, color):
        """Liste sekmesi oluştur"""
        movies = self.user_lists.get(list_key, [])

        if not movies:
            empty_label = ctk.CTkLabel(
                parent,
                text="Bu liste henüz boş 📭",
                font=ctk.CTkFont(size=18),
                text_color=COLORS['text_secondary']
            )
            empty_label.pack(expand=True)
            return

        # Liste başlığı ve sayısı
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        count_label = ctk.CTkLabel(
            header_frame,
            text=f"Toplam: {len(movies)} film",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=color
        )
        count_label.pack(side="left")

        clear_btn = ctk.CTkButton(
            header_frame,
            text="🗑️ Listeyi Temizle",
            command=lambda: self.clear_list(list_key),
            fg_color=COLORS['error'],
            width=120,
            height=30
        )
        clear_btn.pack(side="right")

        # Scrollable liste
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        for movie_title in movies:
            self.create_list_item(scroll_frame, movie_title, list_key, color)

    def create_list_item(self, parent, movie_title, list_key, color):
        """Liste öğesi oluştur"""
        item_frame = ctk.CTkFrame(parent, height=60, corner_radius=10)
        item_frame.pack(fill="x", pady=5)
        item_frame.pack_propagate(False)

        # Film adı
        title_label = ctk.CTkLabel(
            item_frame,
            text=movie_title,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left", padx=20, pady=15, fill="x", expand=True)

        # Butonlar
        button_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=15, pady=10)

        details_btn = ctk.CTkButton(
            button_frame,
            text="👁️",
            command=lambda: self.show_movie_details(movie_title),
            width=35,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        details_btn.pack(side="left", padx=2)

        remove_btn = ctk.CTkButton(
            button_frame,
            text="🗑️",
            command=lambda: self.remove_from_list(list_key, movie_title),
            width=35,
            height=35,
            fg_color=COLORS['error'],
            font=ctk.CTkFont(size=12)
        )
        remove_btn.pack(side="left", padx=2)

    def clear_list(self, list_key):
        """Listeyi temizle"""
        list_names = {
            'liked': 'Beğendiklerim',
            'disliked': 'Beğenmediklerim',
            'watched': 'İzlediklerim',
            'to_watch': 'İzleyeceklerim',
            'favorites': 'Favorilerim'
        }

        # Onay penceresi için geçici bir Toplevel pencere oluştur
        confirm_window = ctk.CTkToplevel()
        confirm_window.title("Onay")
        confirm_window.geometry("400x200")
        confirm_window.resizable(False, False)
        confirm_window.lift()
        confirm_window.attributes('-topmost', True)
        confirm_window.focus()
        confirm_window.grab_set()

        # Pencereyi merkeze al
        confirm_window.transient(self.main_window)

        # Ana frame
        main_frame = ctk.CTkFrame(confirm_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Mesaj
        message_label = ctk.CTkLabel(
            main_frame,
            text=f"{list_names[list_key]} listesini tamamen temizlemek\nistediğinizden emin misiniz?",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        message_label.pack(pady=(30, 40))

        # Buton frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=(0, 20))

        def confirm_action():
            # Listeyi temizle
            self.user_lists[list_key] = []
            self.load_user_lists()

            # Onay penceresini kapat
            confirm_window.grab_release()
            confirm_window.destroy()

            # Başarı mesajı göster - ön katmanda
            temp_root = tk.Tk()
            temp_root.withdraw()
            temp_root.attributes('-topmost', True)
            messagebox.showinfo("Başarılı", f"{list_names[list_key]} listesi temizlendi!", parent=temp_root)
            temp_root.destroy()

            # Mevcut liste pencerelerini bul ve kapat
            for widget in self.main_window.winfo_children():
                if isinstance(widget, ctk.CTkToplevel):
                    if "Film Listelerim" in widget.title():
                        widget.destroy()
                        break

            # Liste penceresini yeniden aç
            self.main_window.after(1, self.show_lists)  # Kısa bir gecikme ile aç

        def cancel_action():
            confirm_window.grab_release()
            confirm_window.destroy()

        # Evet butonu
        yes_btn = ctk.CTkButton(
            button_frame,
            text="Evet",
            command=confirm_action,
            fg_color=COLORS['error'],
            width=100
        )
        yes_btn.pack(side="left", padx=(0, 10))

        # Hayır butonu
        no_btn = ctk.CTkButton(
            button_frame,
            text="Hayır",
            command=cancel_action,
            fg_color=COLORS['secondary'],
            width=100
        )
        no_btn.pack(side="left")

        # Pencere kapatma eventi
        confirm_window.protocol("WM_DELETE_WINDOW", cancel_action)
    def show_profile(self):
        """Profil ekranı"""
        profile_window = ctk.CTkToplevel(self.main_window)
        profile_window.title("Profil")
        profile_window.geometry("500x600")
        profile_window.resizable(False, False)
        profile_window.lift()
        profile_window.attributes('-topmost', True)
        profile_window.focus()

        # Ana frame
        main_frame = ctk.CTkFrame(profile_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Profil başlığı
        title_label = ctk.CTkLabel(
            main_frame,
            text="👤 Profil Bilgileri",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS['accent']
        )
        title_label.pack(pady=(30, 40))

        # Kullanıcı bilgileri
        info_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        info_frame.pack(fill="x", padx=20, pady=(0, 30))

        user_label = ctk.CTkLabel(
            info_frame,
            text=f"Kullanıcı: {self.current_user}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        user_label.pack(pady=20)

        # İstatistikler
        stats_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        stats_frame.pack(fill="x", padx=20, pady=(0, 30))

        stats_title = ctk.CTkLabel(
            stats_frame,
            text="📊 İstatistikler",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS['accent']
        )
        stats_title.pack(pady=(20, 15))

        stats_data = [
            ("👍 Beğenilen Filmler", len(self.user_lists.get('liked', []))),
            ("👎 Beğenilmeyen Filmler", len(self.user_lists.get('disliked', []))),
            ("✅ İzlenen Filmler", len(self.user_lists.get('watched', []))),
            ("📝 İzlenecek Filmler", len(self.user_lists.get('to_watch', []))),
            ("⭐ Favori Filmler", len(self.user_lists.get('favorites', [])))
        ]

        for stat_name, count in stats_data:
            stat_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_frame.pack(fill="x", padx=20, pady=5)

            stat_label = ctk.CTkLabel(
                stat_frame,
                text=stat_name,
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            stat_label.pack(side="left")

            count_label = ctk.CTkLabel(
                stat_frame,
                text=str(count),
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=COLORS['accent']
            )
            count_label.pack(side="right")

        # Butonlar
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)

        export_btn = self.create_modern_button(
            button_frame,
            "📄 Listeleri Dışa Aktar",
            self.export_lists,
            COLORS['primary']
        )
        export_btn.pack(fill="x", pady=(0, 10))

        import_btn = self.create_modern_button(
            button_frame,
            "📥 Listeleri İçe Aktar",
            self.import_lists,
            COLORS['success']
        )
        import_btn.pack(fill="x")

    def export_lists(self):
        """Listeleri dışa aktar"""
        try:
            filename = f"{self.current_user}_movie_lists.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.user_lists, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Başarılı", f"Listeleriniz {filename} dosyasına aktarıldı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Dışa aktarma başarısız: {e}")

    def import_lists(self):
        """Listeleri içe aktar"""
        try:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                title="Liste dosyasını seçin",
                filetypes=[("JSON files", "*.json")]
            )
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    imported_lists = json.load(f)

                # Mevcut listelerle birleştir
                for key in self.user_lists:
                    if key in imported_lists:
                        for movie in imported_lists[key]:
                            if movie not in self.user_lists[key]:
                                self.user_lists[key].append(movie)

                self.save_user_lists()
                messagebox.showinfo("Başarılı", "Listeler başarıyla içe aktarıldı!")
        except Exception as e:
            messagebox.showerror("Hata", f"İçe aktarma başarısız: {e}")

    # Kullanıcı yönetimi metodları
    def login(self):
        """Kullanıcı girişi"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz!")
            return

        users = self.load_users()
        if username in users and users[username] == password:
            self.current_user = username
            self.load_user_lists()
            self.login_window.destroy()
            self.show_main_window()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre!")

    def register(self):
        """Kullanıcı kaydı"""
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm = self.reg_confirm_entry.get()

        if not username or not password:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz!")
            return

        if len(username) < 3:
            messagebox.showerror("Hata", "Kullanıcı adı en az 3 karakter olmalı!")
            return

        if len(password) < 6:
            messagebox.showerror("Hata", "Şifre en az 6 karakter olmalı!")
            return

        if password != confirm:
            messagebox.showerror("Hata", "Şifreler eşleşmiyor!")
            return

        users = self.load_users()
        if username in users:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut!")
            return

        users[username] = password
        self.save_users(users)
        messagebox.showinfo("Başarılı", "Hesap başarıyla oluşturuldu!")
        self.register_window.destroy()
        self.show_login_window()

    def back_to_login(self):
        """Giriş ekranına dön"""
        self.register_window.destroy()
        self.show_login_window()

    def logout(self):
        """Çıkış yap"""
        result = messagebox.askyesno("Çıkış", "Çıkış yapmak istediğinizden emin misiniz?")
        if result:
            self.main_window.destroy()
            self.current_user = None
            self.user_lists = {
                'liked': [],
                'disliked': [],
                'watched': [],
                'to_watch': [],
                'favorites': []
            }
            self.show_login_window()

    # Veri yönetimi metodları
    def load_users(self):
        """Kullanıcıları yükle"""
        try:
            if os.path.exists(USER_DATA_FILE):
                with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}

    def save_users(self, users):
        """Kullanıcıları kaydet"""
        try:
            with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcı kaydetme hatası: {e}")

    def load_user_lists(self):
        try:
            if os.path.exists(USER_LISTS_FILE):
                with open(USER_LISTS_FILE, 'r', encoding='utf-8') as f:
                    all_lists = json.load(f)
                    if self.current_user in all_lists:
                        # Varsayılan yapıyı koru
                        default_lists = {
                            'liked': [],
                            'disliked': [],
                            'watched': [],
                            'to_watch': [],
                            'favorites': []
                        }
                        user_lists = all_lists[self.current_user]
                        # Eksik anahtarları ekle
                        for key in default_lists:
                            if key not in user_lists:
                                user_lists[key] = []
                        self.user_lists = user_lists
        except Exception as e:
            messagebox.showerror("Hata", f"Liste yükleme hatası: {e}")
# Ana uygulama başlatma
if __name__ == "__main__":
    app = ModernMovieApp()
    app.show_login_window()