#QUERIES FOR KITSU GRAPHQL API

BASE_URL = "https://kitsu.io/api/graphql"


# ================ ANIME ================

ANIME_BY_ID: str = """
            query animeByID($id: ID!) {
                findAnimeById(id: $id) {
                    id
                    slug
                    createdAt
                    updatedAt
                    startDate
                    endDate
                    description
                    status
                    sfw
                    animesub: subtype
                    ageRating
                    endDate
                    season
                    episodeCount
                    episodeLength
                    totalLength
                    youtubeTrailerVideoId
                    averageRatingRank
                    averageRating
                    userCountRank
                    titles{
                        canonical
                        localized
                    }
                    posterImage {
                        original {
                            url
                        }
                        views {
                            name
                            url
                        }
                    }
                    bannerImage {
                    original {
                        url
                    }
                    views {
                        name
                        url
                    }      
                    }
                }
            }
"""

ANIME_BY_ID_EPISODES: str = """
            query episodes ($id: ID!, $limit: Int!) {
                findAnimeById(id: $id) {
                episodes (first: $limit) {
                nodes {
                    id
                    length
                    number
                    titles {
                        canonical
                        localized
                    }
                    description
                    thumbnail {
                        original {
                            url
                        }
                    }
                    }
                }
                }
            } 
"""

ANIME_BY_ID_REVIEWS: str = """
            query reviews ($id: ID!, $limit: Int!) {
                findAnimeById(id: $id) {
                reactions (first: $limit) {
                nodes {
                    id
                    progress
                    reaction
                }
                }
                }
            }
"""

ANIME_BY_ID_CHARACTERS: str = """
            query characters ($id: ID!, $limit: Int) {
                findAnimeById(id: $id) {
                characters (first: $limit) {
                nodes {
                    role
                    character {
                    createdAt
                    updatedAt
                    id
                    slug
                    description
                    names {
                        canonical
                        localized
                    }
                    image {
                        original {
                        url
                        }
                        views {
                        url
                        }
                    }
                    }
                }
                }
                }
            }
"""

ANIME_BY_ID_CATEGORIES: str = """
            query category ($id: ID!) {
                findAnimeById(id: $id) {
                categories (first: 25) {
                nodes {
                    title
                    slug
                    description
                    isNsfw
                }
                }
                }
            }
"""

ANIME_BY_ID_STREAMLINKS: str =  """
            query streamLinks ($id: ID!) {
                findAnimeById(id: $id) {
                streamingLinks (first: 10) {
                nodes {
                    id
                    streamer {
                        siteName
                    }
                    subs
                    dubs
                    url
                } 
                }
                }
            }
"""

ANIME_BY_TITLE: str = """
        query animeByTitle($title: String!, $limit: Int) {
            searchAnimeByTitle(first: $limit, title: $title) {
            nodes {
                id
                slug
                createdAt
                updatedAt
                startDate
                endDate
                description
                status
                sfw
                animesub: subtype
                ageRating
                endDate
                season
                episodeCount
                episodeLength
                totalLength
                youtubeTrailerVideoId
                averageRatingRank
                averageRating
                userCountRank
                titles{
                    canonical
                    localized
                }
                posterImage {
                    original {
                        url
                    }
                    views {
                        name
                        url
                    }
                }
                bannerImage {
                original {
                    url
                }
                views {
                    name
                    url
                }      
                }
            }
            }
        }
"""

# ================ MANGA ================

MANGA_BY_ID: str = """
        query mangaByID ($id: ID!) {
        findMangaById(id: $id) {
            id
            slug
            createdAt
            updatedAt
            startDate
            endDate
            description
            status
            sfw
            mangasub: subtype
            ageRating
            endDate
            chapterCount
            volumeCount
            averageRatingRank
            averageRating
            userCountRank
            titles{
            canonical
            localized
            }
            posterImage {
            original {
                url
            }
            views {
                name
                url
            }
            }
            bannerImage {
            original {
                url
            }
            views {
                name
                url
            }      
            }
        }

        }
"""

MANGA_BY_ID_CHAPTERS = """
        query chapters ($id: ID!, $limit: Int) {
        findMangaById(id: $id) {
            chapters (first: $limit) {
            nodes {
                id
                createdAt
                updatedAt
                titles {
                romanized
                }

                description
                number
                thumbnail {
                original {
                    url
                }
            }
            }
            }
        }
        }
"""

MANGA_BY_ID_CHARACTERS: str = """
            query characters ($id: ID!, $limit: Int) {
                findMangaById(id: $id) {
                characters (first: $limit) {
                nodes {
                    role
                    character {
                    createdAt
                    updatedAt
                    id
                    slug
                    description
                    names {
                        canonical
                        localized
                    }
                    image {
                        original {
                        url
                        }
                        views {
                        url
                        }
                    }
                    }
                }
                }
                }
            }
"""

MANGA_BY_ID_CATEGORIES: str = """
            query category ($id: ID!) {
                findMangaById(id: $id) {
                categories (first: 25) {
                nodes {
                    title
                    slug
                    description
                    isNsfw
                }
                }
                }
            }
"""

MANGA_BY_ID_REVIEWS: str = """
            query reviews ($id: ID!, $limit: Int!) {
                findAnimeById(id: $id) {
                reactions (first: $limit) {
                nodes {
                    id
                    progress
                    reaction
                }
                }
                }
            }
"""

MANGA_BY_TITLE: str = """
            query mangaByTitle($title: String!, $limit: Int) {
                searchMangaByTitle(first: $limit, title: $title) {
                nodes {
                    id
                        slug
                        createdAt
                        updatedAt
                        startDate
                        endDate
                        description
                        status
                        sfw
                        mangasub: subtype
                        ageRating
                        endDate
                        chapterCount
                        volumeCount
                        averageRatingRank
                        averageRating
                        userCountRank
                        titles{
                        canonical
                        localized
                        }
                        posterImage {
                        original {
                            url
                        }
                        views {
                            name
                            url
                        }
                        }
                        bannerImage {
                        original {
                            url
                        }
                        views {
                            name
                            url
                        }      
                        }
                } 
            }
            }
"""
# ================ USERS ================

USERS_BY_ID: str = """
            query userByID ($id: ID!) {
            findProfileById (id: $id) {
                id
                name
                slug
                birthday 
                about
                location
                waifuOrHusbando
                gender
                proTier
                url
                posts (first: 1) {
                    totalCount
                }
                mediaReactions(first: 1){
                    totalCount
                }
                comments (first: 1) {
                    totalCount
                }
                followers (first: 1){
                    totalCount
                }
                following (first: 1){
                    totalCount
                }
                favorites (first: 1){
                    totalCount
                }
                avatarImage {
                    original {
                        url
                    }
                    views {
                        name
                        url
                    }
                }
                bannerImage {
                    original {
                        url
                    }
                    views {
                        name
                        url
                    }
                }
            }
            }
"""

USERS_BY_ID_SOCIAL = """
            query socials ($id: ID!) {
            findProfileById (id: $id) {
                siteLinks (first: 30) {
                nodes {
                    id
                    url
                }
                }
            }
            }
"""

USER_BY_USERNAME = """
            query userByUsername ($name: String!) {
                searchProfileByUsername (first: 1, username: $name) {
                nodes {
                    id
                    name
                    slug
                    birthday 
                    about
                    location
                    waifuOrHusbando
                    gender
                    url
                        proTier
                    posts (first: 1) {
                        totalCount
                    }
                    mediaReactions(first: 1){
                        totalCount
                    }
                    comments (first: 1) {
                        totalCount
                    }
                    followers (first: 1){
                        totalCount
                    }
                    following (first: 1){
                        totalCount
                    }
                    favorites (first: 1){
                        totalCount
                    }
                    avatarImage {
                        original {
                            url
                        }
                        views {
                            name
                            url
                        }
                    }
                    bannerImage {
                        original {
                            url
                        }
                        views {
                            name
                            url
                        }
                    }
                    }
                    }
            }
"""
# ================ MISC ================

TRENDING_ENTRY = """
            query checkUser ($media: MediaTypeEnum!, $limit: Int) {
            globalTrending (first: $limit, mediaType: $media) {
                nodes {
                ... on Anime {
                        id
                        slug
                        createdAt
                        updatedAt
                        startDate
                        endDate
                        description
                        status
                        sfw
                        animesub: subtype
                        ageRating
                        endDate
                        season
                        episodeCount
                        episodeLength
                        totalLength
                        youtubeTrailerVideoId
                        averageRatingRank
                        averageRating
                        userCountRank
                        titles{
                            canonical
                            localized
                        }
                        posterImage {
                            original {
                                url
                            }
                            views {
                                name
                                url
                            }
                        }
                        bannerImage {
                        original {
                            url
                        }
                        views {
                            name
                            url
                        }      
                        }
                }
                ... on Manga {
                                id
                        slug
                        createdAt
                        updatedAt
                        startDate
                        endDate
                        description
                        status
                        sfw
                        mangasub: subtype
                        ageRating
                        endDate
                        chapterCount
                        volumeCount
                        averageRatingRank
                        averageRating
                        userCountRank
                        titles{
                        canonical
                        localized
                        }
                        posterImage {
                        original {
                            url
                        }
                        views {
                            name
                            url
                        }
                        }
                        bannerImage {
                        original {
                            url
                        }
                        views {
                            name
                            url
                        }      
                        }
                }
                }
            }
            }
"""

# ================ METHODS ================

QUERY_METHODS = {
    "anime_search": "searchAnimeByTitle",
    "manga_search": "searchMangaByTitle",
    "anime_id": "findAnimeById",
    "manga_id": "findMangaById",
    #"character_search": "findCharacterBySlug"
}

ENTRY_TITLE = {
    "searchAnimeByTitle" : ANIME_BY_TITLE,
    "searchMangaByTitle" : MANGA_BY_TITLE,
}

ENTRY_ID = {
    "findAnimeById" : ANIME_BY_ID,
    "findMangaById" : MANGA_BY_ID,
}

ENTRY_ID_REVIEWS = {
    "findAnimeById" : ANIME_BY_ID_REVIEWS,
    "findMangaById" : MANGA_BY_ID_REVIEWS,   
}

ENTRY_ID_CHARACTERS = {
    "findAnimeById" : ANIME_BY_ID_CHARACTERS,
    "findMangaById" : MANGA_BY_ID_CHARACTERS,
}